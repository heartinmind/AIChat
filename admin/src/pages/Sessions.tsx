import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  InputAdornment,
  IconButton,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tabs,
  Tab,
  LinearProgress,
  Grid,
  Avatar,
  Divider,
} from '@mui/material';
import {
  Search,
  FilterList,
  Refresh,
  Chat,
  SmartToy,
  SupportAgent,
  AccessTime,
  CheckCircle,
  Cancel,
  Download,
  Person,
} from '@mui/icons-material';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { api } from '../contexts/AuthContext';
import { useSnackbar } from 'notistack';

interface Session {
  session_id: string;
  user_name: string;
  agent_name: string | null;
  started_at: string;
  ended_at: string | null;
  status: 'active' | 'ended' | 'failed';
  route_target: 'ai' | 'agent';
  message_count?: number;
  duration?: string;
}

interface Message {
  message_id: string;
  sender: 'user' | 'agent' | 'ai';
  content: string;
  timestamp: string;
  emotion_tag?: string;
}

const Sessions: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selectedSession, setSelectedSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [dateFilter, setDateFilter] = useState<Date | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);

  const fetchSessions = async () => {
    setIsLoading(true);
    try {
      const response = await api.get('/api/admin/sessions', {
        params: {
          limit: 100,
          // 실제로는 필터 파라미터 추가
        },
      });
      
      // 더미 데이터 추가 (실제로는 API에서 모든 정보를 받아야 함)
      const enrichedSessions = response.data.map((session: any) => ({
        ...session,
        message_count: Math.floor(Math.random() * 50) + 5,
        duration: `${Math.floor(Math.random() * 60)}분`,
      }));
      
      setSessions(enrichedSessions);
    } catch (error) {
      enqueueSnackbar('세션 목록을 불러오는데 실패했습니다', { variant: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const fetchSessionMessages = async (sessionId: string) => {
    setIsLoadingMessages(true);
    try {
      const response = await api.get(`/api/sessions/${sessionId}/messages`);
      setMessages(response.data);
    } catch (error) {
      enqueueSnackbar('메시지를 불러오는데 실패했습니다', { variant: 'error' });
    } finally {
      setIsLoadingMessages(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleViewDetails = (session: Session) => {
    setSelectedSession(session);
    setDetailDialogOpen(true);
    fetchSessionMessages(session.session_id);
  };

  const handleExportChat = (session: Session) => {
    // 채팅 내역 다운로드 로직
    enqueueSnackbar('채팅 내역을 다운로드합니다', { variant: 'info' });
  };

  const columns: GridColDef[] = [
    {
      field: 'user_name',
      headerName: '사용자',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Avatar sx={{ width: 32, height: 32 }}>
            {params.value?.[0] || '?'}
          </Avatar>
          <Typography variant="body2">{params.value || '알 수 없음'}</Typography>
        </Box>
      ),
    },
    {
      field: 'route_target',
      headerName: '상담 유형',
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <Chip
          size="small"
          icon={params.value === 'ai' ? <SmartToy /> : <SupportAgent />}
          label={params.value === 'ai' ? 'AI' : '상담원'}
          color={params.value === 'ai' ? 'secondary' : 'primary'}
        />
      ),
    },
    {
      field: 'agent_name',
      headerName: '담당',
      width: 130,
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2">
          {params.row.route_target === 'ai' ? 'AI 지수' : (params.value || '-')}
        </Typography>
      ),
    },
    {
      field: 'started_at',
      headerName: '시작 시간',
      width: 180,
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2">
          {format(new Date(params.value), 'yyyy-MM-dd HH:mm', { locale: ko })}
        </Typography>
      ),
    },
    {
      field: 'duration',
      headerName: '상담 시간',
      width: 100,
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2">{params.value || '-'}</Typography>
      ),
    },
    {
      field: 'message_count',
      headerName: '메시지',
      width: 80,
      align: 'center',
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2">{params.value || 0}</Typography>
      ),
    },
    {
      field: 'status',
      headerName: '상태',
      width: 100,
      renderCell: (params: GridRenderCellParams) => {
        const statusConfig = {
          active: { color: 'warning', icon: <AccessTime />, label: '진행중' },
          ended: { color: 'success', icon: <CheckCircle />, label: '완료' },
          failed: { color: 'error', icon: <Cancel />, label: '실패' },
        };
        const config = statusConfig[params.value as keyof typeof statusConfig];
        return (
          <Chip
            size="small"
            icon={config.icon}
            label={config.label}
            color={config.color as any}
          />
        );
      },
    },
    {
      field: 'actions',
      headerName: '작업',
      width: 150,
      sortable: false,
      renderCell: (params: GridRenderCellParams) => (
        <Box>
          <IconButton
            size="small"
            onClick={() => handleViewDetails(params.row as Session)}
            color="primary"
          >
            <Chat />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleExportChat(params.row as Session)}
            color="default"
          >
            <Download />
          </IconButton>
        </Box>
      ),
    },
  ];

  const filteredSessions = sessions.filter(session => {
    if (searchTerm && !session.user_name?.toLowerCase().includes(searchTerm.toLowerCase())) {
      return false;
    }
    if (statusFilter !== 'all' && session.status !== statusFilter) {
      return false;
    }
    if (dateFilter) {
      const sessionDate = new Date(session.started_at);
      if (format(sessionDate, 'yyyy-MM-dd') !== format(dateFilter, 'yyyy-MM-dd')) {
        return false;
      }
    }
    return true;
  });

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          상담 내역
        </Typography>
        <Typography variant="body1" color="text.secondary">
          모든 상담 세션을 조회하고 관리합니다
        </Typography>
      </Box>

      {/* 필터 영역 */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              size="small"
              placeholder="사용자 이름 검색..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <DatePicker
              label="날짜 선택"
              value={dateFilter}
              onChange={(newValue) => setDateFilter(newValue)}
              slotProps={{
                textField: {
                  size: 'small',
                  fullWidth: true,
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <Tabs
              value={statusFilter}
              onChange={(_, value) => setStatusFilter(value)}
              variant="fullWidth"
            >
              <Tab label="전체" value="all" />
              <Tab label="진행중" value="active" />
              <Tab label="완료" value="ended" />
            </Tabs>
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<Refresh />}
              onClick={fetchSessions}
            >
              새로고침
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* 테이블 */}
      <Paper>
        <DataGrid
          rows={filteredSessions}
          columns={columns}
          getRowId={(row) => row.session_id}
          loading={isLoading}
          autoHeight
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 10 },
            },
          }}
          sx={{
            border: 'none',
            '& .MuiDataGrid-cell': {
              borderBottom: '1px solid rgba(224, 224, 224, 0.3)',
            },
          }}
        />
      </Paper>

      {/* 상세 대화 내역 다이얼로그 */}
      <Dialog
        open={detailDialogOpen}
        onClose={() => setDetailDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6">상담 내역 상세</Typography>
            {selectedSession && (
              <Chip
                size="small"
                icon={selectedSession.route_target === 'ai' ? <SmartToy /> : <SupportAgent />}
                label={selectedSession.route_target === 'ai' ? 'AI 상담' : '상담원 상담'}
                color={selectedSession.route_target === 'ai' ? 'secondary' : 'primary'}
              />
            )}
          </Box>
        </DialogTitle>
        <DialogContent dividers>
          {isLoadingMessages ? (
            <LinearProgress />
          ) : (
            <Box sx={{ minHeight: 400, maxHeight: 600, overflow: 'auto' }}>
              {messages.map((message, index) => (
                <Box
                  key={message.message_id}
                  sx={{
                    mb: 2,
                    display: 'flex',
                    justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                  }}
                >
                  <Box
                    sx={{
                      maxWidth: '70%',
                      p: 2,
                      borderRadius: 2,
                      bgcolor: message.sender === 'user' ? 'primary.main' : 'grey.100',
                      color: message.sender === 'user' ? 'white' : 'text.primary',
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      {message.sender === 'user' ? (
                        <Person fontSize="small" />
                      ) : message.sender === 'ai' ? (
                        <SmartToy fontSize="small" />
                      ) : (
                        <SupportAgent fontSize="small" />
                      )}
                      <Typography variant="caption">
                        {message.sender === 'user' ? '사용자' : message.sender === 'ai' ? 'AI' : '상담원'}
                      </Typography>
                      <Typography variant="caption" sx={{ ml: 'auto' }}>
                        {format(new Date(message.timestamp), 'HH:mm', { locale: ko })}
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                      {message.content}
                    </Typography>
                    {message.emotion_tag && (
                      <Chip
                        size="small"
                        label={message.emotion_tag}
                        sx={{ mt: 1 }}
                        variant="outlined"
                      />
                    )}
                  </Box>
                </Box>
              ))}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailDialogOpen(false)}>닫기</Button>
          <Button
            variant="contained"
            startIcon={<Download />}
            onClick={() => handleExportChat(selectedSession!)}
          >
            내보내기
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Sessions;
