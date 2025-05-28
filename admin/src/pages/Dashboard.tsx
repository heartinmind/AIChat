import React, { useEffect, useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp,
  People,
  Chat,
  SupportAgent,
  Refresh,
  AccessTime,
  CheckCircle,
  Cancel,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { format, subDays, startOfDay } from 'date-fns';
import { ko } from 'date-fns/locale';
import { api } from '../contexts/AuthContext';
import { useSnackbar } from 'notistack';

interface DashboardStats {
  today_sessions: number;
  active_sessions: number;
  total_users: number;
  active_agents: number;
}

interface SessionTrend {
  date: string;
  ai_sessions: number;
  agent_sessions: number;
  total: number;
}

interface RouteDistribution {
  name: string;
  value: number;
  color: string;
}

const Dashboard: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [sessionTrends, setSessionTrends] = useState<SessionTrend[]>([]);
  const [routeDistribution, setRouteDistribution] = useState<RouteDistribution[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchDashboardData = async () => {
    try {
      setRefreshing(true);
      
      // 대시보드 통계
      const statsResponse = await api.get('/api/admin/dashboard');
      setStats(statsResponse.data);

      // 세션 트렌드 (더미 데이터 - 실제로는 API에서 가져와야 함)
      const trends: SessionTrend[] = [];
      for (let i = 6; i >= 0; i--) {
        const date = format(subDays(new Date(), i), 'MM/dd', { locale: ko });
        trends.push({
          date,
          ai_sessions: Math.floor(Math.random() * 50) + 30,
          agent_sessions: Math.floor(Math.random() * 30) + 10,
          total: 0,
        });
      }
      trends.forEach(t => t.total = t.ai_sessions + t.agent_sessions);
      setSessionTrends(trends);

      // 라우팅 분포
      setRouteDistribution([
        { name: 'AI 상담', value: 65, color: '#9C27B0' },
        { name: '상담원 상담', value: 35, color: '#E91E63' },
      ]);

      enqueueSnackbar('대시보드를 업데이트했습니다', { variant: 'success' });
    } catch (error) {
      enqueueSnackbar('데이터 로드 중 오류가 발생했습니다', { variant: 'error' });
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (isLoading) {
    return <LinearProgress />;
  }

  const StatCard: React.FC<{
    title: string;
    value: number;
    icon: React.ReactNode;
    color: string;
    trend?: number;
  }> = ({ title, value, icon, color, trend }) => (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Box>
            <Typography color="text.secondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
              {value.toLocaleString()}
            </Typography>
            {trend !== undefined && (
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TrendingUp sx={{ fontSize: 16, color: trend > 0 ? 'success.main' : 'error.main' }} />
                <Typography
                  variant="body2"
                  sx={{
                    ml: 0.5,
                    color: trend > 0 ? 'success.main' : 'error.main',
                  }}
                >
                  {trend > 0 ? '+' : ''}{trend}%
                </Typography>
              </Box>
            )}
          </Box>
          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: `${color}.100`,
              color: `${color}.main`,
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            대시보드
          </Typography>
          <Typography variant="body1" color="text.secondary">
            실시간 상담 현황 및 통계
          </Typography>
        </Box>
        <Tooltip title="새로고침">
          <IconButton onClick={fetchDashboardData} disabled={refreshing}>
            <Refresh sx={{ animation: refreshing ? 'spin 1s linear infinite' : 'none' }} />
          </IconButton>
        </Tooltip>
      </Box>

      {/* 통계 카드 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="오늘 상담"
            value={stats?.today_sessions || 0}
            icon={<Chat />}
            color="primary"
            trend={12}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="진행 중 상담"
            value={stats?.active_sessions || 0}
            icon={<AccessTime />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="전체 사용자"
            value={stats?.total_users || 0}
            icon={<People />}
            color="info"
            trend={8}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="활성 상담원"
            value={stats?.active_agents || 0}
            icon={<SupportAgent />}
            color="success"
          />
        </Grid>
      </Grid>

      {/* 차트 영역 */}
      <Grid container spacing={3}>
        {/* 상담 트렌드 */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              주간 상담 트렌드
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={sessionTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="ai_sessions"
                  stackId="1"
                  stroke="#9C27B0"
                  fill="#9C27B0"
                  fillOpacity={0.6}
                  name="AI 상담"
                />
                <Area
                  type="monotone"
                  dataKey="agent_sessions"
                  stackId="1"
                  stroke="#E91E63"
                  fill="#E91E63"
                  fillOpacity={0.6}
                  name="상담원 상담"
                />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 상담 유형 분포 */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              상담 유형 분포
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={routeDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {routeDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 최근 활동 */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              최근 활동
            </Typography>
            <Box sx={{ mt: 2 }}>
              {[1, 2, 3, 4, 5].map((i) => (
                <Box
                  key={i}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    py: 2,
                    borderBottom: i < 5 ? '1px solid' : 'none',
                    borderColor: 'divider',
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <CheckCircle color="success" />
                    <Box>
                      <Typography variant="body1">
                        새로운 상담 시작 - 김민수님
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        AI 상담으로 라우팅됨
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {i}분 전
                  </Typography>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>

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

export default Dashboard;
