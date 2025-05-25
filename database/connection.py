# 🔌 데이터베이스 연결 설정
# PostgreSQL 및 Firestore 연결 관리

import os
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import BaseQuery
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference

# 환경변수에서 설정 로드
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# ================================
# PostgreSQL 설정
# ================================

class PostgreSQLManager:
    """PostgreSQL 데이터베이스 연결 관리자"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            # 개별 환경변수로 URL 구성
            user = os.getenv('POSTGRES_USER', 'beauty_clinic_user')
            password = os.getenv('POSTGRES_PASSWORD', 'password')
            host = os.getenv('POSTGRES_HOST', 'localhost')
            port = os.getenv('POSTGRES_PORT', '5432')
            dbname = os.getenv('POSTGRES_DB', 'beauty_clinic_db')
            self.database_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        
        # SQLAlchemy 엔진 생성
        self.engine = create_engine(
            self.database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=os.getenv('DEBUG', 'false').lower() == 'true'
        )
        
        # 세션 팩토리 생성
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info("PostgreSQL 연결 설정 완료")
    
    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        """데이터베이스 세션 컨텍스트 매니저"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"데이터베이스 오류: {e}")
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """테이블 생성"""
        from .models import Base
        Base.metadata.create_all(bind=self.engine)
        logger.info("데이터베이스 테이블 생성 완료")
    
    def test_connection(self) -> bool:
        """연결 테스트"""
        try:
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
                logger.info("PostgreSQL 연결 테스트 성공")
                return True
        except Exception as e:
            logger.error(f"PostgreSQL 연결 실패: {e}")
            return False

# ================================
# Firestore 설정
# ================================

class FirestoreManager:
    """Firestore 데이터베이스 연결 관리자"""
    
    def __init__(self):
        self.client: Optional[firestore.Client] = None
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'elite-cms-2025')
        self.credentials_path = os.getenv('GCS_CREDENTIALS_PATH')
        
        self._initialize_firestore()
    
    def _initialize_firestore(self):
        """Firestore 초기화"""
        try:
            # Firebase Admin SDK 초기화 확인
            if not firebase_admin._apps:
                if self.credentials_path and os.path.exists(self.credentials_path):
                    # 서비스 계정 키 파일 사용
                    cred = credentials.Certificate(self.credentials_path)
                    firebase_admin.initialize_app(cred, {
                        'projectId': self.project_id
                    })
                else:
                    # 기본 자격 증명 사용 (Google Cloud 환경)
                    firebase_admin.initialize_app()
            
            self.client = firestore.client()
            logger.info("Firestore 연결 설정 완료")
            
        except Exception as e:
            logger.error(f"Firestore 초기화 실패: {e}")
            self.client = None
    
    def get_collection(self, collection_name: str) -> Optional[CollectionReference]:
        """컬렉션 참조 반환"""
        if not self.client:
            logger.error("Firestore 클라이언트가 초기화되지 않음")
            return None
        return self.client.collection(collection_name)
    
    def get_document(self, collection_name: str, document_id: str) -> Optional[DocumentReference]:
        """문서 참조 반환"""
        collection = self.get_collection(collection_name)
        if not collection:
            return None
        return collection.document(document_id)
    
    def test_connection(self) -> bool:
        """연결 테스트"""
        try:
            if not self.client:
                return False
            
            # 테스트 문서 작성/읽기
            test_doc = self.client.collection('_test').document('connection_test')
            test_doc.set({'test': True, 'timestamp': firestore.SERVER_TIMESTAMP})
            
            # 문서 읽기
            doc = test_doc.get()
            if doc.exists:
                # 테스트 문서 삭제
                test_doc.delete()
                logger.info("Firestore 연결 테스트 성공")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Firestore 연결 실패: {e}")
            return False

# ================================
# 통합 데이터베이스 매니저
# ================================

class DatabaseManager:
    """PostgreSQL과 Firestore를 통합 관리하는 클래스"""
    
    def __init__(self, use_postgresql: bool = True, use_firestore: bool = True):
        self.use_postgresql = use_postgresql
        self.use_firestore = use_firestore
        
        self.postgresql: Optional[PostgreSQLManager] = None
        self.firestore: Optional[FirestoreManager] = None
        
        if use_postgresql:
            self.postgresql = PostgreSQLManager()
        
        if use_firestore:
            self.firestore = FirestoreManager()
    
    def initialize_databases(self):
        """데이터베이스 초기화"""
        if self.postgresql:
            self.postgresql.create_tables()
        
        # Firestore는 스키마가 없으므로 초기화 불필요
        logger.info("데이터베이스 초기화 완료")
    
    def test_all_connections(self) -> Dict[str, bool]:
        """모든 데이터베이스 연결 테스트"""
        results = {}
        
        if self.postgresql:
            results['postgresql'] = self.postgresql.test_connection()
        
        if self.firestore:
            results['firestore'] = self.firestore.test_connection()
        
        return results
    
    def get_postgresql_session(self):
        """PostgreSQL 세션 반환"""
        if not self.postgresql:
            raise ValueError("PostgreSQL이 초기화되지 않음")
        return self.postgresql.get_db_session()
    
    def get_firestore_client(self):
        """Firestore 클라이언트 반환"""
        if not self.firestore or not self.firestore.client:
            raise ValueError("Firestore가 초기화되지 않음")
        return self.firestore.client

# ================================
# 전역 인스턴스
# ================================

# 환경변수로 사용할 데이터베이스 결정
USE_POSTGRESQL = os.getenv('USE_POSTGRESQL', 'true').lower() == 'true'
USE_FIRESTORE = os.getenv('USE_FIRESTORE', 'true').lower() == 'true'

# 전역 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager(
    use_postgresql=USE_POSTGRESQL,
    use_firestore=USE_FIRESTORE
)

# ================================
# 편의 함수들
# ================================

def get_postgresql_session():
    """PostgreSQL 세션 컨텍스트 매니저 반환"""
    return db_manager.get_postgresql_session()

def get_firestore_client():
    """Firestore 클라이언트 반환"""
    return db_manager.get_firestore_client()

def init_databases():
    """데이터베이스 초기화"""
    db_manager.initialize_databases()

def test_connections():
    """모든 데이터베이스 연결 테스트"""
    return db_manager.test_all_connections()

# ================================
# 헬스체크 함수
# ================================

def health_check() -> Dict[str, Any]:
    """데이터베이스 상태 확인"""
    try:
        connection_results = test_connections()
        
        health_status = {
            'status': 'healthy' if all(connection_results.values()) else 'unhealthy',
            'databases': connection_results,
            'timestamp': str(firestore.SERVER_TIMESTAMP),
            'details': {}
        }
        
        # PostgreSQL 상세 정보
        if db_manager.postgresql:
            try:
                with get_postgresql_session() as session:
                    result = session.execute("SELECT version()").fetchone()
                    health_status['details']['postgresql_version'] = result[0] if result else 'unknown'
            except Exception as e:
                health_status['details']['postgresql_error'] = str(e)
        
        # Firestore 상세 정보
        if db_manager.firestore and db_manager.firestore.client:
            health_status['details']['firestore_project'] = db_manager.firestore.project_id
        
        return health_status
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': str(firestore.SERVER_TIMESTAMP)
        }

# ================================
# 사용 예시
# ================================

if __name__ == "__main__":
    # 연결 테스트
    print("🔍 데이터베이스 연결 테스트 중...")
    results = test_connections()
    
    for db_name, status in results.items():
        emoji = "✅" if status else "❌"
        print(f"{emoji} {db_name}: {'연결 성공' if status else '연결 실패'}")
    
    # 헬스체크
    print("\n🏥 헬스체크 실행 중...")
    health = health_check()
    print(f"상태: {health['status']}")
    
    if health.get('details'):
        for key, value in health['details'].items():
            print(f"  {key}: {value}")
