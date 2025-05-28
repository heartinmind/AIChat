import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Avatar,
  Chip,
  IconButton,
  Switch,
  FormControlLabel,
  Card,
  CardContent,
  CardActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  InputAdornment,
} from '@mui/material';
import {
  PersonAdd,
  Edit,
  Delete,
  Visibility,
  VisibilityOff,
  CheckCircle,
  Cancel,
  AccessTime,
  TrendingUp,
  Email,
  Lock,
  Person,
  Work,
  AdminPanelSettings,
} from '@mui/icons-material';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import { api } from '../contexts/AuthContext';
import { useSnackbar } from 'notistack';

interface Agent {
  agent_id: string;
  name: string;
  email: string;
  department: string;
  status: 'active' | 'offline' | 'on_call';
  last_active: string;
  is_admin: boolean;
  created_at: string;
  handled_sessions: number;
  avg_rating: number;
  response_time: string;
}

interface AgentFormData {
  name: string;
  email: string;
  password: string;
  department: string;
  is_admin: boolean;
}

const Agents: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  
  const [formData, setFormData] = useState<AgentFormData>({
    name: '',
    email: '',
    password: '',
    department: '',
    is_admin: false,
  });

  const fetchAgents = async () => {
    setIsLoading(true);
    try {
      // 실제로는 API에서 상담원 목록을 가져와야 함
      // 더미 데이터 생성
      const dummyAgents: Agent[] = [
        {
          agent_id: '1',
          name: '김상담',
          email: 'kim@elitebeauty.com',
          department: '피부과',
          status: 'active',
          last_active: '2024-02-20T16:45:00',
          is_admin: true,
          created_at: '2023-12-01T09:00:00',
          handled_sessions: 245,
          avg_rating: 4.8,
          response_time: '2분 30초',
        },
        {
          agent_id: '2',
          name: '이미용',
          email: 'lee@elitebeauty.com',
          department: '미용',
          status: 'on_call',
          last_active: '2024-02-20T16:40:00',
          is_admin: false,
          created_at: '2024-01-15T10:00:00',
          handled_sessions: 156,
          avg_rating: 4.9,
          response_time: '1분 45초',
        },
        {
          agent_id: '3',
          name: '박관리',
          email: 'park@elitebeauty.com',
          department: '관리팀',
          status: 'offline',
          last_active: '2024-02-19T18:00:00',
          is_admin: false,
          created_at: '2024-01-20T11:00:00',
          handled_sessions: 89,
          avg_rating: 4.7,
          response_time: '3분 15초',
        },
      ];
      
      setAgents(dummyAgents);
    } catch (error) {
      enqueueSnackbar('상담원 목록을 불러오는데 실패했습니다', { variant: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleAddAgent = async () => {
    try {
      // API 호출
      // await api.post('/api/agents', formData);
      enqueueSnackbar('상담원이 추가되었습니다', { variant: 'success' });
      setAddDialogOpen(false);
      resetForm();
      fetchAgents();
    } catch (error) {
      enqueueSnackbar('상담원 추가에 실패했습니다', { variant: 'error' });
    }
  };

  const handleEditAgent = async () => {
    try {
      // API 호출
      // await api.put(`/api/agents/${selectedAgent?.agent_id}`, formData);
      enqueueSnackbar('상담원 정보가 수정되었습니다', { variant: 'success' });
      setEditDialogOpen(false);
      resetForm();
      fetchAgents();
    } catch (error) {
      enqueueSnackbar('상담원 정보 수정에 실패했습니다', { variant: 'error' });
    }
  };

  const handleDeleteAgent = async (agentId: string) => {
    if (window.confirm('정말로 이 상담원을 삭제하시겠습니까?')) {
      try {
        // API 호출
        // await api.delete(`/api/agents/${agentId}`);
        enqueueSnackbar('상담원이 삭제되었습니다', { variant: 'success' });
        fetchAgents();
      } catch (error) {
        enqueueSnackbar('상담원 삭제에 실패했습니다', { variant: 'error' });
      }
    }
  };

  const handleStatusChange = async (agentId: string, newStatus: string) => {
    try {
      // API 호출
      // await api.patch(`/api/agents/${agentId}/status`, { status: newStatus });
      enqueueSnackbar('상태가 변경되었습니다', { variant: 'success' });
      fetchAgents();
    } catch (error) {
      enqueueSnackbar('상태 변경에 실패했습니다', { variant: 'error' });
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      email: '',
      password: '',
      department: '',
      is_admin: false,
    });
    setSelectedAgent(null);
  };

  const openEditDialog = (agent: Agent) => {
    setSelectedAgent(agent);
    setFormData({
      name: agent.name,
      email: agent.email,
      password: '',
      department: agent.department,
      is_admin: agent.is_admin,
    });
    setEditDialogOpen(true);
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
          <Box>
            <Typography variant="body2">{params.value}</Typography>
            {params.row.is_admin && (
              <Chip
                size="small"
                label="관리자"
                icon={<AdminPanelSettings />}
                sx={{ height: 20, fontSize: '0.7rem' }}
              />
            )}
          </Box>
        </Box>
      ),
    },
    {
      field: 'email',
      headerName: '이메일',
      width: 200,
      renderCell: (params: GridRenderCellParams) => (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Email fontSize="small" color="action" />
          <Typography variant="body2">{params.value}</Typography>
        </Box>
      ),
    },
    {
      field: 'department',
      headerName: '부서',
      width: 120,
      renderCell: (params: GridRenderCellParams) => (
        <Chip size="small" label={params.value} variant="outlined" />
      ),
    },
    {
      field: 'status',
      headerName: '상태',
      width: 120,
      renderCell: (params: GridRenderCellParams) => {
        const statusConfig = {
          active: { color: 'success', icon: <CheckCircle />, label: '활성' },
          on_call: { color: 'warning', icon: <AccessTime />, label: '상담중' },
          offline: { color: 'default', icon: <Cancel />, label: '오프라인' },
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
      field: 'handled_sessions',
      headerName: '처리 상담',
      width: 100,
      align: 'center',
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2">{params.value}건</Typography>
      ),
    },
    {
      field: 'avg_rating',
      headerName: '평점',
      width: 100,
      align: 'center',
      renderCell: (params: GridRenderCellParams) => (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Typography variant="body2" sx={{ fontWeight: 600 }}>
            {params.value}
          </Typography>
          <Typography variant="body2" color="text.secondary">/ 5.0</Typography>
        </Box>
      ),
    },
    {
      field: 'response_time',
      headerName: '평균 응답',
      width: 120,
      align: 'center',
    },
    {
      field: 'last_active',
      headerName: '마지막 활동',
      width: 150,
      renderCell: (params: GridRenderCellParams) => {
        const lastActive = new Date(params.value);
        const now = new Date();
        const diffMinutes = Math.floor((now.getTime() - lastActive.getTime()) / (1000 * 60));
        
        let displayText = '';
        if (diffMinutes < 60) {
          displayText = `${diffMinutes}분 전`;
        } else if (diffMinutes < 1440) {
          displayText = `${Math.floor(diffMinutes / 60)}시간 전`;
        } else {
          displayText = format(lastActive, 'MM/dd HH:mm', { locale: ko });
        }
        
        return (
          <Typography variant="body2" color={diffMinutes < 10 ? 'success.main' : 'text.secondary'}>
            {displayText}
          </Typography>
        );
      },
    },
    {
      field: 'actions',
      headerName: '작업',
      width: 120,
      sortable: false,
      renderCell: (params: GridRenderCellParams) => (
        <Box>
          <IconButton
            size="small"
            onClick={() => openEditDialog(params.row as Agent)}
            color="primary"
          >
            <Edit />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleDeleteAgent(params.row.agent_id)}
            color="error"
          >
            <Delete />
          </IconButton>
        </Box>
      ),
    },
  ];

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            상담원 관리
          </Typography>
          <Typography variant="body1" color="text.secondary">
            상담원을 추가하고 권한을 관리합니다
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<PersonAdd />}
          onClick={() => setAddDialogOpen(true)}
        >
          상담원 추가
        </Button>
      </Box>

      {/* 통계 카드 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                전체 상담원
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                {agents.length}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                등록된 상담원
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                활성 상담원
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, color: 'success.main' }}>
                {agents.filter(a => a.status === 'active').length}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                현재 대기중
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                평균 평점
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                {(agents.reduce((acc, a) => acc + a.avg_rating, 0) / agents.length).toFixed(1)}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TrendingUp fontSize="small" color="success" />
                <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                  +0.2 이번 달
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                평균 응답시간
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                2분 15초
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                첫 응답까지
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 테이블 */}
      <Paper>
        <DataGrid
          rows={agents}
          columns={columns}
          getRowId={(row) => row.agent_id}
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

      {/* 상담원 추가/수정 다이얼로그 */}
      <Dialog
        open={addDialogOpen || editDialogOpen}
        onClose={() => {
          setAddDialogOpen(false);
          setEditDialogOpen(false);
          resetForm();
        }}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {addDialogOpen ? '새 상담원 추가' : '상담원 정보 수정'}
        </DialogTitle>
        <DialogContent dividers>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="이름"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Person />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="이메일"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Email />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label={editDialogOpen ? '새 비밀번호 (변경시에만)' : '비밀번호'}
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Lock />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>부서</InputLabel>
                <Select
                  value={formData.department}
                  label="부서"
                  onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                  startAdornment={
                    <InputAdornment position="start">
                      <Work />
                    </InputAdornment>
                  }
                >
                  <MenuItem value="피부과">피부과</MenuItem>
                  <MenuItem value="미용">미용</MenuItem>
                  <MenuItem value="관리팀">관리팀</MenuItem>
                  <MenuItem value="상담팀">상담팀</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={formData.is_admin}
                    onChange={(e) => setFormData({ ...formData, is_admin: e.target.checked })}
                  />
                }
                label="관리자 권한 부여"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setAddDialogOpen(false);
            setEditDialogOpen(false);
            resetForm();
          }}>
            취소
          </Button>
          <Button
            variant="contained"
            onClick={addDialogOpen ? handleAddAgent : handleEditAgent}
          >
            {addDialogOpen ? '추가' : '수정'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Agents;
