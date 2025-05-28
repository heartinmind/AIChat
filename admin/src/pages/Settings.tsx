import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Grid,
  Divider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  IconButton,
  InputAdornment,
  Tabs,
  Tab,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormGroup,
  Slider,
  Tooltip,
} from '@mui/material';
import {
  Save,
  Visibility,
  VisibilityOff,
  Key,
  Add,
  Delete,
  Edit,
  ContentCopy,
  Check,
  Refresh,
  Security,
  Notifications,
  Business,
  SmartToy,
  Warning,
} from '@mui/icons-material';
import { useSnackbar } from 'notistack';
import { api } from '../contexts/AuthContext';

interface GeneralSettings {
  clinicName: string;
  clinicAddress: string;
  clinicPhone: string;
  clinicEmail: string;
  businessHours: {
    weekday: string;
    weekend: string;
  };
  holidayNotice: string;
}

interface AISettings {
  model: string;
  temperature: number;
  maxTokens: number;
  responseStyle: string;
  language: string;
  contextWindow: number;
  fallbackBehavior: string;
}

interface NotificationSettings {
  emailNotifications: boolean;
  smsNotifications: boolean;
  dashboardAlerts: boolean;
  dailyReport: boolean;
  weeklyReport: boolean;
  criticalAlerts: boolean;
}

interface SecuritySettings {
  twoFactorAuth: boolean;
  sessionTimeout: number;
  ipWhitelist: boolean;
  allowedIPs: string[];
  passwordPolicy: {
    minLength: number;
    requireUppercase: boolean;
    requireNumbers: boolean;
    requireSpecialChars: boolean;
  };
}

interface APIKey {
  id: string;
  name: string;
  key: string;
  created: string;
  lastUsed: string;
  status: 'active' | 'inactive';
}

const Settings: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [currentTab, setCurrentTab] = useState(0);
  const [isSaving, setIsSaving] = useState(false);
  const [showApiKey, setShowApiKey] = useState<{ [key: string]: boolean }>({});
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [apiKeyDialogOpen, setApiKeyDialogOpen] = useState(false);
  const [newApiKeyName, setNewApiKeyName] = useState('');

  // Settings state
  const [generalSettings, setGeneralSettings] = useState<GeneralSettings>({
    clinicName: 'Elite Beauty Clinic',
    clinicAddress: '서울특별시 강남구 청담동 123-45',
    clinicPhone: '02-1234-5678',
    clinicEmail: 'info@elitebeauty.com',
    businessHours: {
      weekday: '09:00 - 19:00',
      weekend: '10:00 - 17:00',
    },
    holidayNotice: '일요일 및 공휴일 휴무',
  });

  const [aiSettings, setAISettings] = useState<AISettings>({
    model: 'claude-3-opus',
    temperature: 0.7,
    maxTokens: 2048,
    responseStyle: 'professional',
    language: 'ko',
    contextWindow: 8192,
    fallbackBehavior: 'transfer',
  });

  const [notificationSettings, setNotificationSettings] = useState<NotificationSettings>({
    emailNotifications: true,
    smsNotifications: false,
    dashboardAlerts: true,
    dailyReport: false,
    weeklyReport: true,
    criticalAlerts: true,
  });

  const [securitySettings, setSecuritySettings] = useState<SecuritySettings>({
    twoFactorAuth: false,
    sessionTimeout: 30,
    ipWhitelist: false,
    allowedIPs: [],
    passwordPolicy: {
      minLength: 8,
      requireUppercase: true,
      requireNumbers: true,
      requireSpecialChars: false,
    },
  });

  const [apiKeys, setApiKeys] = useState<APIKey[]>([
    {
      id: '1',
      name: 'Production API Key',
      key: 'sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxx',
      created: '2024-05-01',
      lastUsed: '2024-05-28',
      status: 'active',
    },
    {
      id: '2',
      name: 'Development API Key',
      key: 'sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxx',
      created: '2024-04-15',
      lastUsed: '2024-05-25',
      status: 'active',
    },
  ]);

  const handleSaveSettings = async () => {
    try {
      setIsSaving(true);
      // API 호출하여 설정 저장
      await new Promise(resolve => setTimeout(resolve, 1000)); // 시뮬레이션
      enqueueSnackbar('설정이 저장되었습니다', { variant: 'success' });
    } catch (error) {
      enqueueSnackbar('설정 저장 중 오류가 발생했습니다', { variant: 'error' });
    } finally {
      setIsSaving(false);
    }
  };

  const handleCopyApiKey = (key: string, id: string) => {
    navigator.clipboard.writeText(key);
    setCopiedKey(id);
    setTimeout(() => setCopiedKey(null), 2000);
    enqueueSnackbar('API 키가 클립보드에 복사되었습니다', { variant: 'success' });
  };

  const handleCreateApiKey = () => {
    const newKey: APIKey = {
      id: Date.now().toString(),
      name: newApiKeyName,
      key: 'sk_live_' + Math.random().toString(36).substring(2, 15),
      created: new Date().toISOString().split('T')[0],
      lastUsed: '-',
      status: 'active',
    };
    setApiKeys([...apiKeys, newKey]);
    setApiKeyDialogOpen(false);
    setNewApiKeyName('');
    enqueueSnackbar('새 API 키가 생성되었습니다', { variant: 'success' });
  };

  const handleDeleteApiKey = (id: string) => {
    setApiKeys(apiKeys.filter(key => key.id !== id));
    enqueueSnackbar('API 키가 삭제되었습니다', { variant: 'success' });
  };

  const handleToggleApiKeyStatus = (id: string) => {
    setApiKeys(apiKeys.map(key => 
      key.id === id 
        ? { ...key, status: key.status === 'active' ? 'inactive' : 'active' }
        : key
    ));
  };

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          설정
        </Typography>
        <Typography variant="body1" color="text.secondary">
          시스템 설정 및 환경 구성
        </Typography>
      </Box>

      {/* 탭 */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={currentTab} onChange={(e, v) => setCurrentTab(v)}>
          <Tab icon={<Business />} label="일반 설정" />
          <Tab icon={<SmartToy />} label="AI 설정" />
          <Tab icon={<Notifications />} label="알림 설정" />
          <Tab icon={<Security />} label="보안 설정" />
          <Tab icon={<Key />} label="API 키" />
        </Tabs>
      </Paper>

      {/* 일반 설정 */}
      {currentTab === 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            병원 정보
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="병원명"
                value={generalSettings.clinicName}
                onChange={(e) => setGeneralSettings({ ...generalSettings, clinicName: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="대표 전화번호"
                value={generalSettings.clinicPhone}
                onChange={(e) => setGeneralSettings({ ...generalSettings, clinicPhone: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="주소"
                value={generalSettings.clinicAddress}
                onChange={(e) => setGeneralSettings({ ...generalSettings, clinicAddress: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="이메일"
                type="email"
                value={generalSettings.clinicEmail}
                onChange={(e) => setGeneralSettings({ ...generalSettings, clinicEmail: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="휴무 안내"
                value={generalSettings.holidayNotice}
                onChange={(e) => setGeneralSettings({ ...generalSettings, holidayNotice: e.target.value })}
              />
            </Grid>
          </Grid>

          <Divider sx={{ my: 4 }} />

          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            영업 시간
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="평일 영업시간"
                value={generalSettings.businessHours.weekday}
                onChange={(e) => setGeneralSettings({
                  ...generalSettings,
                  businessHours: { ...generalSettings.businessHours, weekday: e.target.value }
                })}
                helperText="예: 09:00 - 19:00"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="주말 영업시간"
                value={generalSettings.businessHours.weekend}
                onChange={(e) => setGeneralSettings({
                  ...generalSettings,
                  businessHours: { ...generalSettings.businessHours, weekend: e.target.value }
                })}
                helperText="예: 10:00 - 17:00"
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleSaveSettings}
              disabled={isSaving}
            >
              저장
            </Button>
          </Box>
        </Paper>
      )}

      {/* AI 설정 */}
      {currentTab === 1 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            AI 모델 설정
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>AI 모델</InputLabel>
                <Select
                  value={aiSettings.model}
                  label="AI 모델"
                  onChange={(e) => setAISettings({ ...aiSettings, model: e.target.value })}
                >
                  <MenuItem value="claude-3-opus">Claude 3 Opus</MenuItem>
                  <MenuItem value="claude-3-sonnet">Claude 3 Sonnet</MenuItem>
                  <MenuItem value="gpt-4">GPT-4</MenuItem>
                  <MenuItem value="gpt-3.5-turbo">GPT-3.5 Turbo</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>응답 스타일</InputLabel>
                <Select
                  value={aiSettings.responseStyle}
                  label="응답 스타일"
                  onChange={(e) => setAISettings({ ...aiSettings, responseStyle: e.target.value })}
                >
                  <MenuItem value="professional">전문적</MenuItem>
                  <MenuItem value="friendly">친근함</MenuItem>
                  <MenuItem value="concise">간결함</MenuItem>
                  <MenuItem value="detailed">상세함</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography gutterBottom>Temperature: {aiSettings.temperature}</Typography>
              <Slider
                value={aiSettings.temperature}
                onChange={(e, v) => setAISettings({ ...aiSettings, temperature: v as number })}
                min={0}
                max={1}
                step={0.1}
                marks
                valueLabelDisplay="auto"
              />
              <Typography variant="caption" color="text.secondary">
                낮을수록 일관성 있고, 높을수록 창의적인 응답
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="최대 토큰 수"
                value={aiSettings.maxTokens}
                onChange={(e) => setAISettings({ ...aiSettings, maxTokens: parseInt(e.target.value) })}
                InputProps={{
                  inputProps: { min: 100, max: 4096 }
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>언어</InputLabel>
                <Select
                  value={aiSettings.language}
                  label="언어"
                  onChange={(e) => setAISettings({ ...aiSettings, language: e.target.value })}
                >
                  <MenuItem value="ko">한국어</MenuItem>
                  <MenuItem value="en">영어</MenuItem>
                  <MenuItem value="ja">일본어</MenuItem>
                  <MenuItem value="zh">중국어</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>폴백 동작</InputLabel>
                <Select
                  value={aiSettings.fallbackBehavior}
                  label="폴백 동작"
                  onChange={(e) => setAISettings({ ...aiSettings, fallbackBehavior: e.target.value })}
                >
                  <MenuItem value="transfer">상담원에게 전달</MenuItem>
                  <MenuItem value="retry">재시도</MenuItem>
                  <MenuItem value="default">기본 응답</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleSaveSettings}
              disabled={isSaving}
            >
              저장
            </Button>
          </Box>
        </Paper>
      )}

      {/* 알림 설정 */}
      {currentTab === 2 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            알림 채널
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  checked={notificationSettings.emailNotifications}
                  onChange={(e) => setNotificationSettings({
                    ...notificationSettings,
                    emailNotifications: e.target.checked
                  })}
                />
              }
              label="이메일 알림"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={notificationSettings.smsNotifications}
                  onChange={(e) => setNotificationSettings({
                    ...notificationSettings,
                    smsNotifications: e.target.checked
                  })}
                />
              }
              label="SMS 알림"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={notificationSettings.dashboardAlerts}
                  onChange={(e) => setNotificationSettings({
                    ...notificationSettings,
                    dashboardAlerts: e.target.checked
                  })}
                />
              }
              label="대시보드 알림"
            />
          </FormGroup>

          <Divider sx={{ my: 4 }} />

          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            리포트 설정
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  checked={notificationSettings.dailyReport}
                  onChange={(e) => setNotificationSettings({
                    ...notificationSettings,
                    dailyReport: e.target.checked
                  })}
                />
              }
              label="일일 리포트"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={notificationSettings.weeklyReport}
                  onChange={(e) => setNotificationSettings({
                    ...notificationSettings,
                    weeklyReport: e.target.checked
                  })}
                />
              }
              label="주간 리포트"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={notificationSettings.criticalAlerts}
                  onChange={(e) => setNotificationSettings({
                    ...notificationSettings,
                    criticalAlerts: e.target.checked
                  })}
                />
              }
              label="긴급 알림 (시스템 오류, 보안 이슈 등)"
            />
          </FormGroup>

          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleSaveSettings}
              disabled={isSaving}
            >
              저장
            </Button>
          </Box>
        </Paper>
      )}

      {/* 보안 설정 */}
      {currentTab === 3 && (
        <Paper sx={{ p: 3 }}>
          <Alert severity="warning" sx={{ mb: 3 }}>
            보안 설정 변경은 시스템 전체에 영향을 미칩니다. 신중하게 설정해주세요.
          </Alert>

          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            인증 설정
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={
                <Switch
                  checked={securitySettings.twoFactorAuth}
                  onChange={(e) => setSecuritySettings({
                    ...securitySettings,
                    twoFactorAuth: e.target.checked
                  })}
                />
              }
              label="2단계 인증 (2FA) 사용"
            />
          </FormGroup>

          <Box sx={{ mt: 3, mb: 3 }}>
            <Typography gutterBottom>세션 타임아웃 (분)</Typography>
            <Slider
              value={securitySettings.sessionTimeout}
              onChange={(e, v) => setSecuritySettings({
                ...securitySettings,
                sessionTimeout: v as number
              })}
              min={5}
              max={120}
              step={5}
              marks
              valueLabelDisplay="auto"
            />
          </Box>

          <Divider sx={{ my: 4 }} />

          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            비밀번호 정책
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="최소 길이"
                value={securitySettings.passwordPolicy.minLength}
                onChange={(e) => setSecuritySettings({
                  ...securitySettings,
                  passwordPolicy: {
                    ...securitySettings.passwordPolicy,
                    minLength: parseInt(e.target.value)
                  }
                })}
                InputProps={{
                  inputProps: { min: 6, max: 20 }
                }}
              />
            </Grid>
            <Grid item xs={12}>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={securitySettings.passwordPolicy.requireUppercase}
                      onChange={(e) => setSecuritySettings({
                        ...securitySettings,
                        passwordPolicy: {
                          ...securitySettings.passwordPolicy,
                          requireUppercase: e.target.checked
                        }
                      })}
                    />
                  }
                  label="대문자 포함 필수"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={securitySettings.passwordPolicy.requireNumbers}
                      onChange={(e) => setSecuritySettings({
                        ...securitySettings,
                        passwordPolicy: {
                          ...securitySettings.passwordPolicy,
                          requireNumbers: e.target.checked
                        }
                      })}
                    />
                  }
                  label="숫자 포함 필수"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={securitySettings.passwordPolicy.requireSpecialChars}
                      onChange={(e) => setSecuritySettings({
                        ...securitySettings,
                        passwordPolicy: {
                          ...securitySettings.passwordPolicy,
                          requireSpecialChars: e.target.checked
                        }
                      })}
                    />
                  }
                  label="특수문자 포함 필수"
                />
              </FormGroup>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleSaveSettings}
              disabled={isSaving}
            >
              저장
            </Button>
          </Box>
        </Paper>
      )}

      {/* API 키 관리 */}
      {currentTab === 4 && (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6">
              API 키 관리
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setApiKeyDialogOpen(true)}
            >
              새 API 키
            </Button>
          </Box>

          <Alert severity="info" sx={{ mb: 3 }}>
            API 키는 외부 시스템과 연동할 때 사용됩니다. 키는 안전하게 보관하고 절대 공개하지 마세요.
          </Alert>

          <List>
            {apiKeys.map((apiKey) => (
              <Card key={apiKey.id} sx={{ mb: 2 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box sx={{ flexGrow: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        <Typography variant="h6">{apiKey.name}</Typography>
                        <Chip
                          label={apiKey.status === 'active' ? '활성' : '비활성'}
                          color={apiKey.status === 'active' ? 'success' : 'default'}
                          size="small"
                        />
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                        <TextField
                          value={apiKey.key}
                          type={showApiKey[apiKey.id] ? 'text' : 'password'}
                          InputProps={{
                            readOnly: true,
                            endAdornment: (
                              <InputAdornment position="end">
                                <IconButton
                                  onClick={() => setShowApiKey({
                                    ...showApiKey,
                                    [apiKey.id]: !showApiKey[apiKey.id]
                                  })}
                                  edge="end"
                                >
                                  {showApiKey[apiKey.id] ? <VisibilityOff /> : <Visibility />}
                                </IconButton>
                              </InputAdornment>
                            ),
                          }}
                          size="small"
                          sx={{ width: 400 }}
                        />
                        <Tooltip title="복사">
                          <IconButton onClick={() => handleCopyApiKey(apiKey.key, apiKey.id)}>
                            {copiedKey === apiKey.id ? <Check /> : <ContentCopy />}
                          </IconButton>
                        </Tooltip>
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        생성일: {apiKey.created} | 마지막 사용: {apiKey.lastUsed}
                      </Typography>
                    </Box>
                    <Box>
                      <Tooltip title={apiKey.status === 'active' ? '비활성화' : '활성화'}>
                        <IconButton onClick={() => handleToggleApiKeyStatus(apiKey.id)}>
                          <Refresh />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="삭제">
                        <IconButton onClick={() => handleDeleteApiKey(apiKey.id)} color="error">
                          <Delete />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </List>
        </Paper>
      )}

      {/* API 키 생성 다이얼로그 */}
      <Dialog open={apiKeyDialogOpen} onClose={() => setApiKeyDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>새 API 키 생성</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="API 키 이름"
            value={newApiKeyName}
            onChange={(e) => setNewApiKeyName(e.target.value)}
            placeholder="예: Production API Key"
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setApiKeyDialogOpen(false)}>취소</Button>
          <Button
            variant="contained"
            onClick={handleCreateApiKey}
            disabled={!newApiKeyName.trim()}
          >
            생성
          </Button>
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

export default Settings;
