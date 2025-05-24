/**
 * Configuration settings for Beauty Clinic Chatbot
 * 엘리트 뷰티 클리닉 상담봇 설정
 */

export const config = {
  // API 설정
  api: {
    defaultPageSize: 100,
    maxRetries: 3,
    timeout: 30000,
    baseUrl: process.env.API_BASE_URL || 'http://localhost:8081'
  },
  
  // 뷰티 클리닉 설정
  clinic: {
    name: '엘리트 뷰티 클리닉',
    location: '강남점',
    address: '서울특별시 강남구 강남대로 123',
    phone: '+82-2-1234-5678',
    businessHours: {
      open: '09:00',
      close: '20:00',
      timezone: 'Asia/Seoul'
    }
  },
  
  // 고객 서비스 설정
  customerService: {
    defaultCustomerId: '123',
    sessionTimeout: 1800000, // 30분
    maxConcurrentSessions: 100,
    supportedLanguages: ['ko', 'en'],
    defaultLanguage: 'ko'
  },
  
  // 시술 관련 설정
  treatments: {
    categories: ['botox', 'filler', 'laser', 'facial', 'skincare'] as const,
    maxAppointmentsPerDay: 50,
    defaultDuration: 60, // 분
    bookingAdvanceDays: 30
  },
  
  // 알림 설정
  notifications: {
    reminderTimes: ['24h', '2h', '30min'] as const,
    defaultMethods: ['email', 'sms', 'push'] as const,
    retryAttempts: 3
  },
  
  // 모바일 앱 설정
  mobile: {
    deepLinkScheme: 'elitebeauty',
    pushNotificationEnabled: true,
    syncInterval: 300000, // 5분
    maxOfflineTime: 86400000 // 24시간
  },
  
  // 결제 설정
  payment: {
    currency: 'KRW',
    maxDiscountPercentage: 10,
    maxDiscountAmount: 20000,
    acceptedMethods: ['card', 'cash', 'transfer'] as const
  },
  
  // 보안 설정
  security: {
    maxLoginAttempts: 5,
    sessionTokenLength: 32,
    passwordMinLength: 8,
    dataRetentionDays: 2555 // 7년
  },
  
  // 로깅 설정
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    maxFileSize: '10MB',
    maxFiles: 5,
    logToConsole: process.env.NODE_ENV !== 'production'
  },
  
  // 테스트 설정
  testing: {
    mockData: true,
    testCustomerId: 'test-123',
    testTimeout: 10000
  }
};

// 타입 정의
export type TreatmentCategory = typeof config.treatments.categories[number];
export type ReminderTime = typeof config.notifications.reminderTimes[number];
export type NotificationMethod = typeof config.notifications.defaultMethods[number];
export type PaymentMethod = typeof config.payment.acceptedMethods[number];

// 유틸리티 함수들
export const getBusinessHours = () => {
  return `${config.clinic.businessHours.open} - ${config.clinic.businessHours.close}`;
};

export const isBusinessHours = (time: Date = new Date()): boolean => {
  const hours = time.getHours();
  const openHour = parseInt(config.clinic.businessHours.open.split(':')[0]);
  const closeHour = parseInt(config.clinic.businessHours.close.split(':')[0]);
  
  return hours >= openHour && hours < closeHour;
};

export const formatPrice = (amount: number): string => {
  return `${amount.toLocaleString('ko-KR')}원`;
};

export const getMaxDiscount = (type: 'percentage' | 'amount'): number => {
  return type === 'percentage' 
    ? config.payment.maxDiscountPercentage 
    : config.payment.maxDiscountAmount;
};

// 환경별 설정 오버라이드
export const getEnvironmentConfig = () => {
  const env = process.env.NODE_ENV || 'development';
  
  const envConfigs = {
    development: {
      api: {
        ...config.api,
        timeout: 60000 // 개발 환경에서는 더 긴 타임아웃
      },
      logging: {
        ...config.logging,
        level: 'debug'
      }
    },
    production: {
      api: {
        ...config.api,
        timeout: 15000 // 프로덕션에서는 더 짧은 타임아웃
      },
      logging: {
        ...config.logging,
        level: 'warn',
        logToConsole: false
      }
    },
    test: {
      ...config,
      testing: {
        ...config.testing,
        mockData: true
      }
    }
  };
  
  return { ...config, ...envConfigs[env as keyof typeof envConfigs] };
};

export default config; 
