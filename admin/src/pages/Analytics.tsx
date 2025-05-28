import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Rating,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp,
  AccessTime,
  Mood,
  Person,
  Refresh,
  Download,
  CalendarMonth,
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
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { format, subDays, subMonths } from 'date-fns';
import { ko } from 'date-fns/locale';
import { api } from '../contexts/AuthContext';
import { useSnackbar } from 'notistack';

interface PerformanceMetric {
  label: string;
  value: number | string;
  change: number;
  icon: React.ReactNode;
  color: string;
}

interface ConsultationTopic {
  topic: string;
  count: number;
  percentage: number;
}

interface AgentPerformance {
  id: string;
  name: string;
  sessions: number;
  avgDuration: number;
  satisfaction: number;
  responseTime: number;
}

interface TimePattern {
  hour: string;
  sessions: number;
}

const Analytics: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [period, setPeriod] = useState<'week' | 'month' | 'year'>('month');
  
  // State for analytics data
  const [metrics, setMetrics] = useState<PerformanceMetric[]>([]);
  const [topicDistribution, setTopicDistribution] = useState<ConsultationTopic[]>([]);
  const [agentPerformance, setAgentPerformance] = useState<AgentPerformance[]>([]);
  const [timePatterns, setTimePatterns] = useState<TimePattern[]>([]);
  const [monthlyTrend, setMonthlyTrend] = useState<any[]>([]);
  const [satisfactionTrend, setSatisfactionTrend] = useState<any[]>([]);

  const fetchAnalyticsData = async () => {
    try {
      setRefreshing(true);
      
      // 성과 지표
      setMetrics([
        {
          label: '평균 상담 시간',
          value: '12분 35초',
          change: -5.2,
          icon: <AccessTime />,
          color: 'primary',
        },
        {
          label: '평균 만족도',
          value: 4.6,
          change: 2.3,
          icon: <Mood />,
          color: 'success',
        },
        {
          label: '전환율',
          value: '68.5%',
          change: 8.7,
          icon: <TrendingUp />,
          color: 'info',
        },
        {
          label: '재상담율',
          value: '23.4%',
          change: -3.1,
          icon: <Person />,
          color: 'warning',
        },
      ]);

      // 인기 상담 주제
      setTopicDistribution([
        { topic: '시술 문의', count: 342, percentage: 28.5 },
        { topic: '예약 변경', count: 289, percentage: 24.1 },
        { topic: '가격 문의', count: 198, percentage: 16.5 },
        { topic: '부작용 상담', count: 156, percentage: 13.0 },
        { topic: '시술 후 관리', count: 123, percentage: 10.3 },
        { topic: '기타', count: 92, percentage: 7.6 },
      ]);

      // 상담원별 성과
      setAgentPerformance([
        { id: '1', name: '김미소', sessions: 156, avgDuration: 11.5, satisfaction: 4.8, responseTime: 1.2 },
        { id: '2', name: '이정희', sessions: 142, avgDuration: 13.2, satisfaction: 4.7, responseTime: 1.5 },
        { id: '3', name: '박수진', sessions: 138, avgDuration: 12.8, satisfaction: 4.6, responseTime: 1.8 },
        { id: '4', name: '최은영', sessions: 125, avgDuration: 14.1, satisfaction: 4.5, responseTime: 2.1 },
        { id: '5', name: 'AI 상담원', sessions: 639, avgDuration: 8.3, satisfaction: 4.3, responseTime: 0.1 },
      ]);

      // 시간대별 패턴
      const patterns: TimePattern[] = [];
      for (let i = 9; i <= 21; i++) {
        patterns.push({
          hour: `${i}시`,
          sessions: Math.floor(Math.random() * 50) + 10,
        });
      }
      setTimePatterns(patterns);

      // 월별 추이
      const trends: any[] = [];
      for (let i = 5; i >= 0; i--) {
        const date = format(subMonths(new Date(), i), 'yyyy년 MM월', { locale: ko });
        trends.push({
          month: date,
          상담건수: Math.floor(Math.random() * 1000) + 800,
          AI상담: Math.floor(Math.random() * 600) + 400,
          상담원상담: Math.floor(Math.random() * 400) + 200,
        });
      }
      setMonthlyTrend(trends);

      // 만족도 추이
      const satisfactionData: any[] = [];
      for (let i = 29; i >= 0; i--) {
        const date = format(subDays(new Date(), i), 'MM/dd', { locale: ko });
        satisfactionData.push({
          date,
          AI상담: (Math.random() * 0.5 + 4.0).toFixed(1),
          상담원상담: (Math.random() * 0.3 + 4.5).toFixed(1),
        });
      }
      setSatisfactionTrend(satisfactionData);

      enqueueSnackbar('분석 데이터를 업데이트했습니다', { variant: 'success' });
    } catch (error) {
      enqueueSnackbar('데이터 로드 중 오류가 발생했습니다', { variant: 'error' });
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchAnalyticsData();
  }, [period]);

  const handleExport = () => {
    enqueueSnackbar('분석 리포트를 다운로드합니다', { variant: 'info' });
    // 실제 다운로드 로직 구현
  };

  if (isLoading) {
    return <LinearProgress />;
  }

  const COLORS = ['#9C27B0', '#E91E63', '#3F51B5', '#00BCD4', '#4CAF50', '#FF9800'];

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            통계 분석
          </Typography>
          <Typography variant="body1" color="text.secondary">
            상담 성과 및 패턴 분석
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>기간</InputLabel>
            <Select
              value={period}
              label="기간"
              onChange={(e) => setPeriod(e.target.value as 'week' | 'month' | 'year')}
            >
              <MenuItem value="week">주간</MenuItem>
              <MenuItem value="month">월간</MenuItem>
              <MenuItem value="year">연간</MenuItem>
            </Select>
          </FormControl>
          <Tooltip title="데이터 내보내기">
            <IconButton onClick={handleExport}>
              <Download />
            </IconButton>
          </Tooltip>
          <Tooltip title="새로고침">
            <IconButton onClick={fetchAnalyticsData} disabled={refreshing}>
              <Refresh sx={{ animation: refreshing ? 'spin 1s linear infinite' : 'none' }} />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* 주요 성과 지표 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metrics.map((metric) => (
          <Grid item xs={12} sm={6} md={3} key={metric.label}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Box>
                    <Typography color="text.secondary" gutterBottom variant="body2">
                      {metric.label}
                    </Typography>
                    <Typography variant="h4" component="div" sx={{ fontWeight: 700 }}>
                      {metric.value}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      <TrendingUp
                        sx={{
                          fontSize: 16,
                          color: metric.change > 0 ? 'success.main' : 'error.main',
                          transform: metric.change < 0 ? 'rotate(180deg)' : 'none',
                        }}
                      />
                      <Typography
                        variant="body2"
                        sx={{
                          ml: 0.5,
                          color: metric.change > 0 ? 'success.main' : 'error.main',
                        }}
                      >
                        {Math.abs(metric.change)}%
                      </Typography>
                    </Box>
                  </Box>
                  <Box
                    sx={{
                      width: 56,
                      height: 56,
                      borderRadius: 2,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      bgcolor: `${metric.color}.100`,
                      color: `${metric.color}.main`,
                    }}
                  >
                    {metric.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* 차트 영역 */}
      <Grid container spacing={3}>
        {/* 월별 상담 추이 */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              월별 상담 추이
            </Typography>
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={monthlyTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="AI상담"
                  stackId="1"
                  stroke="#9C27B0"
                  fill="#9C27B0"
                  fillOpacity={0.6}
                />
                <Area
                  type="monotone"
                  dataKey="상담원상담"
                  stackId="1"
                  stroke="#E91E63"
                  fill="#E91E63"
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 인기 상담 주제 */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              인기 상담 주제
            </Typography>
            <ResponsiveContainer width="100%" height={350}>
              <PieChart>
                <Pie
                  data={topicDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ topic, percentage }) => `${topic} ${percentage}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {topicDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 시간대별 상담 패턴 */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              시간대별 상담 패턴
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={timePatterns}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <RechartsTooltip />
                <Bar dataKey="sessions" fill="#3F51B5" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 만족도 추이 */}
        <Grid item xs={12} lg={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              만족도 추이 (30일)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={satisfactionTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[3.5, 5]} />
                <RechartsTooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="AI상담"
                  stroke="#9C27B0"
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="상담원상담"
                  stroke="#E91E63"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* 상담원별 성과 */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              상담원별 성과
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>상담원</TableCell>
                    <TableCell align="right">상담 건수</TableCell>
                    <TableCell align="right">평균 상담시간</TableCell>
                    <TableCell align="center">만족도</TableCell>
                    <TableCell align="right">응답 시간</TableCell>
                    <TableCell align="center">성과</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {agentPerformance.map((agent) => (
                    <TableRow key={agent.id}>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {agent.name}
                          {agent.name === 'AI 상담원' && (
                            <Chip label="AI" size="small" color="primary" />
                          )}
                        </Box>
                      </TableCell>
                      <TableCell align="right">{agent.sessions}건</TableCell>
                      <TableCell align="right">{agent.avgDuration}분</TableCell>
                      <TableCell align="center">
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
                          <Rating value={agent.satisfaction} precision={0.1} readOnly size="small" />
                          <Typography variant="body2">({agent.satisfaction})</Typography>
                        </Box>
                      </TableCell>
                      <TableCell align="right">{agent.responseTime}분</TableCell>
                      <TableCell align="center">
                        <Chip
                          label={agent.satisfaction >= 4.5 ? '우수' : '양호'}
                          color={agent.satisfaction >= 4.5 ? 'success' : 'default'}
                          size="small"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
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

export default Analytics;
