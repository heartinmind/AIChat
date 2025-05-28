import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  InputAdornment,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Avatar,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
} from '@mui/material';
import {
  Search,
  PersonAdd,
  Edit,
  Delete,
  Block,
  CheckCircle,
  Phone,
  CalendarToday,
  Chat,
  TrendingUp,
  Refresh,
} from '@mui/icons-material';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { api } from '../contexts/AuthContext';
import { useSnackbar } from 'notistack';

interface User {
  user_id: string;
  name: string;
  phone: string;
  gender?: string;
  birth_year?: number;
  created_at: string;
  deleted_at?: string;
  session_count: number;
  last_session?: string;
  total_messages: number;
  status: 'active' | 'inactive' | 'blocked';
}

interface UserDetail extends User {
  recent_sessions: {
    session_id: string;
    started_at: string;
    route_target: 'ai' | 'agent';
    status: string;
  }[];
  favorite_treatments?: string[];
}

const Users: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<UserDetail | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);

  const fetchUsers = async () => {
    setIsLoading(true);
    try {
      // 실제로는 API에서 사용자 목록을 가져와야 함
      // 더미 데이터 생성
      const dummyUsers: User[] = [
        {
          user_id: '1',
          name: '김민수',
          phone: '010-1234-5678',
          gender: '남성',
          birth_year: 1990,
          created_at: '2024-01-15T10:00:00',
          session_count: 12,
          last_session: '2024-02-20T14:30:00',
          total_messages: 156,
          status: 'active',
        },
        {
          user_id: '2',
          name: '이영희',
          phone: '010-2345-6789',
          gender: '여성',
          birth_year: 1985,
          created_at: '2024-01-20T11:00:00',
          session_count: 8,
          last_session: '2024-02-19T16:20:00',
          total_messages: 98,
          status: 'active',
        },
        {
          user_id: '3',
          name: '박철수',
          phone: '010-3456-7890',
          gender: '남성',
          birth_year: 1995,
          created_at: '2024-02-01T09:00:00',
          session_count: 3,
          last_session: '2024-02-15T10:00:00',
          total_messages: 45,
          status: 'inactive',
        },
      ];
      
      setUsers(dummyUsers);
    } catch (error) {
      enqueueSnackbar('사용자 목록을 불러오는데 실패했습니다', { variant: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const fetchUserDetail = async (userId: string) => {
    try {
      // 실제로는 API에서 상세 정보를 가져와야 함
      const user = users.find(u => u.user_id === userId);
      if (user) {
        const userDetail: UserDetail = {
          ...user,
          recent_sessions: [
            {
              session_id: '1',
              started_at: '2024-02-20T14:30:00',
              route_target: 'ai',
              status: 'ended',
            },
            {
              session_id: '2',
              started_at: '2024-02-18T11:00:00',
              route_target: 'agent',
              status: 'ended',
            },
          ],
          favorite_treatments: ['보톡스', '필러', '레이저'],
        };
        setSelectedUser(userDetail);
      }
    } catch (error) {
      enqueueSnackbar('사용자 정보를 불러오는데 실패했습니다', { variant: 'error' });
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleViewDetails = (userId: string) => {
    fetchUserDetail(userId);
    setDetailDialogOpen(true);
  };

  const handleEditUser = (userId: string) => {
    fetchUserDetail(userId);
    setEditDialogOpen(true);
  };

  const handleBlockUser = async (userId: string) => {
    if (window.confirm('정말로 이 사용자를 차단하시겠습니까?')) {
      try {
        // API 호출
        enqueueSnackbar('사용자가 차단되었습니다', { variant: 'success' });
        fetchUsers();
      } catch (error) {
        enqueueSnackbar('사용자 차단에 실패했습니다', { variant: 'error' });
      }
    }
  };

  const columns: GridColDef[] = [
    {
      field: 'name',
      headerName: '이름',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Avatar sx={{ width: 32, height: 32 }}>
            {params.value[0]}
          </Avatar>
          <Typography variant="body2">{params.value}</Typography>
        </Box>
      ),
    },
    {
      field: 'phone',
      headerName: '전화번호',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Phone fontSize="small" color="action" />
          <Typography variant="body2">{params.value}</Typography>
        </Box>
      ),
    },
    {
      field: 'gender',
      headerName: '성별',
      width: 80,
      align: 'center',
    },
    {
      field: 'birth_year',
      headerName: '연령대',
      width: 100,
      renderCell: (params: GridRenderCellParams) => {
        if (!params.value) return '-';
        const age = new Date().getFullYear() - params.value;
        return `${Math.floor(age / 10) * 10}대`;
      },
    },
    {
      field: 'created_at',
      headerName: '가입일',
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2">
          {format(new Date(params.value), 'yyyy-MM-dd', { locale: ko })}
        </Typography>
      ),
    },
    {
      field: 'session_count',
      headerName: '상담 횟수',
      width: 100,
      align: 'center',
      renderCell: (params: GridRenderCellParams) => (
        <Chip size="small" label={`${params.value}회`} />
      ),
    },
    {
      field: 'total_messages',
      headerName: '메시지',
      width: 100,
      align: 'center',
    },
    {
      field: 'last_session',
      headerName: '마지막 상담',
      width: 150,
      renderCell: (params: GridRenderCellParams) => {
        if (!params.value) return '-';
        const days = Math.floor((Date.now() - new Date(params.value).getTime()) / (1000 * 60 * 60 * 24));
        return (
          <Typography variant="body2" color={days > 30 ? 'error' : 'text.primary'}>
            {days === 0 ? '오늘' : `${days}일 전`}
          </Typography>
        );
      },
    },
    {
      field: 'status',
      headerName: '상태',
      width: 100,
      renderCell: (params: GridRenderCellParams) => {
        const statusConfig = {
          active: { color: 'success', icon: <CheckCircle />, label: '활성' },
          inactive: { color: 'warning', icon: <Block />, label: '비활성' },
          blocked: { color: 'error', icon: <Block />, label: '차단' },
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
            onClick={() => handleViewDetails(params.row.user_id)}
            color="primary"
          >
            <Search />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleEditUser(params.row.user_id)}
            color="default"
          >
            <Edit />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleBlockUser(params.row.user_id)}
            color="error"
          >
            <Block />
          </IconButton>
        </Box>
      ),
    },
  ];

  const filteredUsers = users.filter(user => {
    if (searchTerm && !user.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
        !user.phone.includes(searchTerm)) {
      return false;
    }
    if (statusFilter !== 'all' && user.status !== statusFilter) {
      return false;
    }
    return true;
  });

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          사용자 관리
        </Typography>
        <Typography variant="body1" color="text.secondary">
          등록된 사용자를 조회하고 관리합니다
        </Typography>
      </Box>

      {/* 통계 카드 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                전체 사용자
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                {users.length}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TrendingUp fontSize="small" color="success" />
                <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                  +12% 이번 달
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                활성 사용자
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                {users.filter(u => u.status === 'active').length}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                최근 30일 이내 상담
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                평균 상담 횟수
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                {(users.reduce((acc, u) => acc + u.session_count, 0) / users.length).toFixed(1)}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                사용자당
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                오늘 신규
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                3
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                신규 가입자
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 필터 영역 */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              size="small"
              placeholder="이름 또는 전화번호로 검색..."
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
            <FormControl fullWidth size="small">
              <InputLabel>상태</InputLabel>
              <Select
                value={statusFilter}
                label="상태"
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="active">활성</MenuItem>
                <MenuItem value="inactive">비활성</MenuItem>
                <MenuItem value="blocked">차단</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<Refresh />}
              onClick={fetchUsers}
            >
              새로고침
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* 테이블 */}
      <Paper>
        <DataGrid
          rows={filteredUsers}
          columns={columns}
          getRowId={(row) => row.user_id}
          loading={isLoading}
          autoHeight
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 10 },
            },
          }}
        />
      </Paper>

      {/* 사용자 상세 정보 다이얼로그 */}
      <Dialog
        open={detailDialogOpen}
        onClose={() => setDetailDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>사용자 상세 정보</DialogTitle>
        <DialogContent dividers>
          {selectedUser && (
            <Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <Avatar sx={{ width: 64, height: 64, fontSize: 28 }}>
                  {selectedUser.name[0]}
                </Avatar>
                <Box>
                  <Typography variant="h6">{selectedUser.name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {selectedUser.phone}
                  </Typography>
                </Box>
              </Box>

              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">성별</Typography>
                  <Typography>{selectedUser.gender || '-'}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">출생년도</Typography>
                  <Typography>{selectedUser.birth_year || '-'}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">가입일</Typography>
                  <Typography>
                    {format(new Date(selectedUser.created_at), 'yyyy-MM-dd', { locale: ko })}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">상태</Typography>
                  <Chip
                    size="small"
                    label={selectedUser.status === 'active' ? '활성' : '비활성'}
                    color={selectedUser.status === 'active' ? 'success' : 'default'}
                  />
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6" gutterBottom>관심 시술</Typography>
              <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
                {selectedUser.favorite_treatments?.map((treatment, index) => (
                  <Chip key={index} label={treatment} size="small" />
                ))}
              </Box>

              <Typography variant="h6" gutterBottom>최근 상담 내역</Typography>
              <List>
                {selectedUser.recent_sessions.map((session, index) => (
                  <React.Fragment key={session.session_id}>
                    <ListItem>
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: session.route_target === 'ai' ? 'secondary.main' : 'primary.main' }}>
                          <Chat />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={`${session.route_target === 'ai' ? 'AI' : '상담원'} 상담`}
                        secondary={format(new Date(session.started_at), 'yyyy-MM-dd HH:mm', { locale: ko })}
                      />
                      <Chip
                        size="small"
                        label={session.status === 'ended' ? '완료' : '진행중'}
                        color={session.status === 'ended' ? 'success' : 'warning'}
                      />
                    </ListItem>
                    {index < selectedUser.recent_sessions.length - 1 && <Divider variant="inset" component="li" />}
                  </React.Fragment>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailDialogOpen(false)}>닫기</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Users;
