import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  LinearProgress,
  Alert,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
} from '@mui/material';
import {
  Upload,
  Delete,
  Edit,
  Refresh,
  Search,
  CloudUpload,
  Description,
  Storage,
  Memory,
  CheckCircle,
  Error,
  Warning,
  Info,
  Sync,
  Download,
  Settings,
} from '@mui/icons-material';
import { useSnackbar } from 'notistack';
import { api } from '../contexts/AuthContext';

interface Document {
  id: string;
  title: string;
  category: string;
  size: string;
  uploadDate: string;
  status: 'indexed' | 'processing' | 'error';
  chunks: number;
  embeddings: number;
}

interface EmbeddingModel {
  id: string;
  name: string;
  provider: string;
  dimension: number;
  status: 'active' | 'inactive';
  documentsProcessed: number;
}

interface KnowledgeBase {
  id: string;
  name: string;
  description: string;
  documentCount: number;
  totalChunks: number;
  lastUpdated: string;
  status: 'synced' | 'updating' | 'error';
}

const RAGManagement: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [currentTab, setCurrentTab] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  
  // Documents state
  const [documents, setDocuments] = useState<Document[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  
  // Embedding models state
  const [embeddingModels, setEmbeddingModels] = useState<EmbeddingModel[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>('');
  
  // Knowledge bases state
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([]);
  const [createKBDialogOpen, setCreateKBDialogOpen] = useState(false);

  const fetchRAGData = async () => {
    try {
      setRefreshing(true);
      
      // 문서 데이터 (더미 데이터)
      setDocuments([
        {
          id: '1',
          title: '피부 시술 가이드 - 레이저 치료',
          category: '시술 안내',
          size: '2.4 MB',
          uploadDate: '2024-05-25',
          status: 'indexed',
          chunks: 156,
          embeddings: 156,
        },
        {
          id: '2',
          title: '보톡스 시술 절차 및 주의사항',
          category: '시술 안내',
          size: '1.8 MB',
          uploadDate: '2024-05-24',
          status: 'indexed',
          chunks: 98,
          embeddings: 98,
        },
        {
          id: '3',
          title: '필러 시술 FAQ',
          category: 'FAQ',
          size: '856 KB',
          uploadDate: '2024-05-23',
          status: 'processing',
          chunks: 45,
          embeddings: 32,
        },
        {
          id: '4',
          title: '피부 타입별 관리법',
          category: '피부 관리',
          size: '3.2 MB',
          uploadDate: '2024-05-22',
          status: 'indexed',
          chunks: 234,
          embeddings: 234,
        },
        {
          id: '5',
          title: '시술 후 주의사항 종합',
          category: '시술 안내',
          size: '1.5 MB',
          uploadDate: '2024-05-21',
          status: 'error',
          chunks: 0,
          embeddings: 0,
        },
      ]);

      // 임베딩 모델 데이터
      setEmbeddingModels([
        {
          id: '1',
          name: 'text-embedding-ada-002',
          provider: 'OpenAI',
          dimension: 1536,
          status: 'active',
          documentsProcessed: 423,
        },
        {
          id: '2',
          name: 'voyage-large-2',
          provider: 'Anthropic',
          dimension: 1024,
          status: 'inactive',
          documentsProcessed: 0,
        },
        {
          id: '3',
          name: 'embed-multilingual-v3.0',
          provider: 'Cohere',
          dimension: 768,
          status: 'inactive',
          documentsProcessed: 0,
        },
      ]);

      // 지식 베이스 데이터
      setKnowledgeBases([
        {
          id: '1',
          name: '시술 정보 KB',
          description: '모든 시술 관련 문서 및 가이드',
          documentCount: 45,
          totalChunks: 1234,
          lastUpdated: '2024-05-25 14:30',
          status: 'synced',
        },
        {
          id: '2',
          name: '고객 FAQ KB',
          description: '자주 묻는 질문과 답변 모음',
          documentCount: 23,
          totalChunks: 456,
          lastUpdated: '2024-05-24 10:15',
          status: 'synced',
        },
        {
          id: '3',
          name: '제품 정보 KB',
          description: '사용 제품 및 화장품 정보',
          documentCount: 18,
          totalChunks: 234,
          lastUpdated: '2024-05-23 16:45',
          status: 'updating',
        },
      ]);

      setSelectedModel('1');
      
      enqueueSnackbar('RAG 데이터를 업데이트했습니다', { variant: 'success' });
    } catch (error) {
      enqueueSnackbar('데이터 로드 중 오류가 발생했습니다', { variant: 'error' });
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchRAGData();
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const handleUploadDocument = () => {
    enqueueSnackbar('문서가 업로드되었습니다', { variant: 'success' });
    setUploadDialogOpen(false);
    // 실제 업로드 로직 구현
  };

  const handleDeleteDocument = (id: string) => {
    enqueueSnackbar('문서가 삭제되었습니다', { variant: 'success' });
    // 실제 삭제 로직 구현
  };

  const handleReindexDocument = (id: string) => {
    enqueueSnackbar('문서 재색인이 시작되었습니다', { variant: 'info' });
    // 실제 재색인 로직 구현
  };

  const handleCreateKnowledgeBase = () => {
    enqueueSnackbar('새 지식 베이스가 생성되었습니다', { variant: 'success' });
    setCreateKBDialogOpen(false);
    // 실제 생성 로직 구현
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'indexed':
      case 'synced':
      case 'active':
        return 'success';
      case 'processing':
      case 'updating':
        return 'warning';
      case 'error':
      case 'inactive':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'indexed':
      case 'synced':
      case 'active':
        return <CheckCircle />;
      case 'processing':
      case 'updating':
        return <Sync />;
      case 'error':
      case 'inactive':
        return <Error />;
      default:
        return <Info />;
    }
  };

  if (isLoading) {
    return <LinearProgress />;
  }

  const filteredDocuments = documents.filter(doc => {
    const matchesSearch = doc.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = categoryFilter === 'all' || doc.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            RAG 관리
          </Typography>
          <Typography variant="body1" color="text.secondary">
            문서 및 임베딩 관리, 지식 베이스 설정
          </Typography>
        </Box>
        <Tooltip title="새로고침">
          <IconButton onClick={fetchRAGData} disabled={refreshing}>
            <Refresh sx={{ animation: refreshing ? 'spin 1s linear infinite' : 'none' }} />
          </IconButton>
        </Tooltip>
      </Box>

      {/* 상태 카드 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    총 문서
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    {documents.length}
                  </Typography>
                </Box>
                <Description sx={{ fontSize: 40, color: 'primary.main', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    총 청크
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    1,924
                  </Typography>
                </Box>
                <Storage sx={{ fontSize: 40, color: 'info.main', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    임베딩 완료
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    1,756
                  </Typography>
                </Box>
                <Memory sx={{ fontSize: 40, color: 'success.main', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="text.secondary" gutterBottom variant="body2">
                    지식 베이스
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    {knowledgeBases.length}
                  </Typography>
                </Box>
                <Storage sx={{ fontSize: 40, color: 'warning.main', opacity: 0.3 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 탭 */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={currentTab} onChange={(e, v) => setCurrentTab(v)}>
          <Tab label="문서 관리" />
          <Tab label="임베딩 설정" />
          <Tab label="지식 베이스" />
        </Tabs>
      </Paper>

      {/* 문서 관리 탭 */}
      {currentTab === 0 && (
        <Paper sx={{ p: 3 }}>
          {/* 검색 및 필터 */}
          <Box sx={{ mb: 3, display: 'flex', gap: 2, alignItems: 'center' }}>
            <TextField
              placeholder="문서 검색..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              size="small"
              sx={{ flexGrow: 1, maxWidth: 400 }}
              InputProps={{
                startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />,
              }}
            />
            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel>카테고리</InputLabel>
              <Select
                value={categoryFilter}
                label="카테고리"
                onChange={(e) => setCategoryFilter(e.target.value)}
              >
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="시술 안내">시술 안내</MenuItem>
                <MenuItem value="FAQ">FAQ</MenuItem>
                <MenuItem value="피부 관리">피부 관리</MenuItem>
              </Select>
            </FormControl>
            <Button
              variant="contained"
              startIcon={<Upload />}
              onClick={() => setUploadDialogOpen(true)}
            >
              문서 업로드
            </Button>
          </Box>

          {/* 문서 테이블 */}
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>문서명</TableCell>
                  <TableCell>카테고리</TableCell>
                  <TableCell>크기</TableCell>
                  <TableCell>업로드 날짜</TableCell>
                  <TableCell align="center">상태</TableCell>
                  <TableCell align="right">청크/임베딩</TableCell>
                  <TableCell align="center">작업</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredDocuments
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((doc) => (
                    <TableRow key={doc.id}>
                      <TableCell>{doc.title}</TableCell>
                      <TableCell>
                        <Chip label={doc.category} size="small" />
                      </TableCell>
                      <TableCell>{doc.size}</TableCell>
                      <TableCell>{doc.uploadDate}</TableCell>
                      <TableCell align="center">
                        <Chip
                          icon={getStatusIcon(doc.status)}
                          label={
                            doc.status === 'indexed' ? '색인 완료' :
                            doc.status === 'processing' ? '처리 중' : '오류'
                          }
                          color={getStatusColor(doc.status)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="right">
                        {doc.chunks} / {doc.embeddings}
                      </TableCell>
                      <TableCell align="center">
                        <Tooltip title="재색인">
                          <IconButton
                            size="small"
                            onClick={() => handleReindexDocument(doc.id)}
                            disabled={doc.status === 'processing'}
                          >
                            <Sync />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="다운로드">
                          <IconButton size="small">
                            <Download />
                          </IconButton>
                        </Tooltip>
                        <Tooltip title="삭제">
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteDocument(doc.id)}
                          >
                            <Delete />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            component="div"
            count={filteredDocuments.length}
            page={page}
            onPageChange={handleChangePage}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            labelRowsPerPage="페이지당 행 수:"
          />
        </Paper>
      )}

      {/* 임베딩 설정 탭 */}
      {currentTab === 1 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            임베딩 모델 설정
          </Typography>
          
          <Alert severity="info" sx={{ mb: 3 }}>
            임베딩 모델을 변경하면 모든 문서를 다시 처리해야 합니다.
          </Alert>

          <Grid container spacing={3}>
            {embeddingModels.map((model) => (
              <Grid item xs={12} md={4} key={model.id}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    border: selectedModel === model.id ? 2 : 1,
                    borderColor: selectedModel === model.id ? 'primary.main' : 'divider',
                  }}
                  onClick={() => setSelectedModel(model.id)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                      <Typography variant="h6">{model.name}</Typography>
                      <Chip
                        label={model.status === 'active' ? '활성' : '비활성'}
                        color={model.status === 'active' ? 'success' : 'default'}
                        size="small"
                      />
                    </Box>
                    <Typography color="text.secondary" gutterBottom>
                      제공: {model.provider}
                    </Typography>
                    <Typography color="text.secondary" gutterBottom>
                      차원: {model.dimension}
                    </Typography>
                    <Typography color="text.secondary">
                      처리 문서: {model.documentsProcessed}개
                    </Typography>
                    {selectedModel === model.id && (
                      <Box sx={{ mt: 2 }}>
                        <Button
                          variant="contained"
                          fullWidth
                          disabled={model.status === 'active'}
                        >
                          {model.status === 'active' ? '현재 사용 중' : '활성화'}
                        </Button>
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              임베딩 설정
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="청크 크기"
                  defaultValue="512"
                  helperText="각 문서 청크의 최대 토큰 수"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="청크 오버랩"
                  defaultValue="50"
                  helperText="청크 간 겹치는 토큰 수"
                />
              </Grid>
              <Grid item xs={12}>
                <Button variant="contained" sx={{ mt: 2 }}>
                  설정 저장
                </Button>
              </Grid>
            </Grid>
          </Box>
        </Paper>
      )}

      {/* 지식 베이스 탭 */}
      {currentTab === 2 && (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6">
              지식 베이스 관리
            </Typography>
            <Button
              variant="contained"
              startIcon={<CloudUpload />}
              onClick={() => setCreateKBDialogOpen(true)}
            >
              새 지식 베이스
            </Button>
          </Box>

          <List>
            {knowledgeBases.map((kb, index) => (
              <React.Fragment key={kb.id}>
                <ListItem>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {kb.name}
                        <Chip
                          label={kb.status === 'synced' ? '동기화됨' : '업데이트 중'}
                          color={getStatusColor(kb.status)}
                          size="small"
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          {kb.description}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          문서: {kb.documentCount}개 | 청크: {kb.totalChunks}개 | 
                          마지막 업데이트: {kb.lastUpdated}
                        </Typography>
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Tooltip title="설정">
                      <IconButton edge="end" sx={{ mr: 1 }}>
                        <Settings />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="동기화">
                      <IconButton edge="end">
                        <Sync />
                      </IconButton>
                    </Tooltip>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < knowledgeBases.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      )}

      {/* 문서 업로드 다이얼로그 */}
      <Dialog open={uploadDialogOpen} onClose={() => setUploadDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>문서 업로드</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="문서 제목"
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>카테고리</InputLabel>
              <Select defaultValue="시술 안내" label="카테고리">
                <MenuItem value="시술 안내">시술 안내</MenuItem>
                <MenuItem value="FAQ">FAQ</MenuItem>
                <MenuItem value="피부 관리">피부 관리</MenuItem>
                <MenuItem value="제품 정보">제품 정보</MenuItem>
              </Select>
            </FormControl>
            <Box
              sx={{
                border: '2px dashed',
                borderColor: 'divider',
                borderRadius: 2,
                p: 4,
                textAlign: 'center',
                cursor: 'pointer',
                '&:hover': {
                  borderColor: 'primary.main',
                  bgcolor: 'action.hover',
                },
              }}
            >
              <CloudUpload sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
              <Typography>
                파일을 드래그하거나 클릭하여 업로드
              </Typography>
              <Typography variant="body2" color="text.secondary">
                PDF, DOC, DOCX, TXT (최대 10MB)
              </Typography>
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>취소</Button>
          <Button variant="contained" onClick={handleUploadDocument}>업로드</Button>
        </DialogActions>
      </Dialog>

      {/* 지식 베이스 생성 다이얼로그 */}
      <Dialog open={createKBDialogOpen} onClose={() => setCreateKBDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>새 지식 베이스 생성</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="지식 베이스 이름"
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="설명"
              multiline
              rows={3}
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth>
              <InputLabel>문서 카테고리 선택</InputLabel>
              <Select
                multiple
                defaultValue={['시술 안내', 'FAQ']}
                label="문서 카테고리 선택"
              >
                <MenuItem value="시술 안내">시술 안내</MenuItem>
                <MenuItem value="FAQ">FAQ</MenuItem>
                <MenuItem value="피부 관리">피부 관리</MenuItem>
                <MenuItem value="제품 정보">제품 정보</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateKBDialogOpen(false)}>취소</Button>
          <Button variant="contained" onClick={handleCreateKnowledgeBase}>생성</Button>
        </DialogActions>
      </Dialog>

      <style>
        {`
          @keyframes spin {
            from {
              transform: rotate(0deg);
            }
            to {
              transform: rotate(360deg);
            }
          }
        `}
      </style>
    </Box>
  );
};

export default RAGManagement;
