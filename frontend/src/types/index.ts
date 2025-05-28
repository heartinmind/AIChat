export interface User {
  user_id: string;
  name: string;
  phone: string;
  gender?: string;
  birth_year?: number;
}

export interface Session {
  session_id: string;
  user_id: string;
  agent_id?: string;
  started_at: string;
  ended_at?: string;
  status: 'active' | 'ended' | 'failed';
  source: 'web' | 'mobile' | 'kakao';
  route_target: 'agent' | 'ai';
}

export interface Message {
  id: string;
  message_id?: string;
  session_id: string;
  sender: 'user' | 'agent' | 'ai' | 'system';
  content: string;
  timestamp: string;
  emotion_tag?: string;
  is_answer?: boolean;
}

export interface RouteResponse {
  target: 'agent' | 'ai';
  reason: string;
}

export interface UserCreateRequest {
  name: string;
  phone: string;
  gender?: string;
  birthYear?: number;
}

export interface SessionCreateRequest {
  user_id: string;
  route_target: string;
  agent_id?: string;
}

export interface MessageCreateRequest {
  session_id: string;
  content: string;
  sender?: string;
}

export interface ClinicInfo {
  id: string;
  category: string;
  subcategory?: string;
  name: string;
  price?: string;
  description?: string;
  duration?: string;
  effect_period?: string;
}