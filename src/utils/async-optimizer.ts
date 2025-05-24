/**
 * Async Processing Optimizer for Beauty Clinic Chatbot
 * 뷰티 클리닉 상담봇 비동기 처리 최적화
 */

import type { 
  BeautyTreatment, 
  Customer, 
  Appointment, 
  TreatmentHistory,
  Satisfaction,
  UUID 
} from '../types';

// 비동기 작업 결과 타입
export interface AsyncResult<T> {
  success: boolean;
  data?: T;
  error?: string;
  executionTime: number;
  fromCache?: boolean;
}

// 배치 작업 결과 타입
export interface BatchResult<T> {
  results: AsyncResult<T>[];
  totalExecutionTime: number;
  successCount: number;
  errorCount: number;
  cacheHitRate: number;
}

// 캐시 항목 타입
interface CacheItem<T> {
  data: T;
  timestamp: number;
  ttl: number;
  accessCount: number;
  lastAccessed: number;
}

// 캐시 통계 타입
interface CacheStats {
  hits: number;
  misses: number;
  hitRate: number;
  totalSize: number;
  memoryUsage: number;
}

export class AsyncOptimizer {
  private readonly maxConcurrency: number;
  private readonly timeout: number;
  private readonly cache: Map<string, CacheItem<any>>;
  private readonly defaultTTL: number;
  private readonly maxCacheSize: number;
  private cacheStats: CacheStats;

  constructor(
    maxConcurrency: number = 10, 
    timeout: number = 30000,
    defaultTTL: number = 300000, // 5분
    maxCacheSize: number = 1000
  ) {
    this.maxConcurrency = maxConcurrency;
    this.timeout = timeout;
    this.cache = new Map();
    this.defaultTTL = defaultTTL;
    this.maxCacheSize = maxCacheSize;
    this.cacheStats = {
      hits: 0,
      misses: 0,
      hitRate: 0,
      totalSize: 0,
      memoryUsage: 0
    };

    // 주기적 캐시 정리 (매 30초)
    setInterval(() => this.cleanupExpiredCache(), 30000);
  }

  /**
   * 캐시 통계 조회
   */
  getCacheStats(): CacheStats {
    this.updateCacheStats();
    return { ...this.cacheStats };
  }

  /**
   * 캐시 초기화
   */
  clearCache(): void {
    this.cache.clear();
    this.cacheStats = {
      hits: 0,
      misses: 0,
      hitRate: 0,
      totalSize: 0,
      memoryUsage: 0
    };
  }

  /**
   * 병렬로 여러 고객 정보를 조회 (캐싱 적용)
   */
  async fetchCustomersParallel(customerIds: UUID[]): Promise<BatchResult<Customer>> {
    const startTime = Date.now();
    
    const batches = this.createBatches(customerIds, this.maxConcurrency);
    const allResults: AsyncResult<Customer>[] = [];

    for (const batch of batches) {
      const batchPromises = batch.map(id => this.fetchCustomerWithCache(id));
      const batchResults = await Promise.all(batchPromises);
      allResults.push(...batchResults);
    }

    return this.createBatchResultWithCache(allResults, startTime);
  }

  /**
   * 병렬로 시술 추천 데이터 조회 (캐싱 적용)
   */
  async fetchTreatmentRecommendationsParallel(
    concerns: string[],
    skinTypes: string[]
  ): Promise<BatchResult<BeautyTreatment[]>> {
    const startTime = Date.now();
    
    const promises = [
      ...concerns.map(concern => this.fetchTreatmentsByConcernWithCache(concern)),
      ...skinTypes.map(skinType => this.fetchTreatmentsBySkinTypeWithCache(skinType))
    ];

    const results = await Promise.allSettled(promises);
    const asyncResults = results.map((result, index) => 
      this.handleSettledResult(result, `Query ${index}`)
    );

    return this.createBatchResultWithCache(asyncResults, startTime);
  }

  /**
   * 고객의 모든 관련 데이터를 병렬로 조회 (캐싱 적용)
   */
  async fetchCustomerCompleteData(customerId: UUID): Promise<{
    customer: AsyncResult<Customer>;
    appointments: AsyncResult<Appointment[]>;
    treatmentHistory: AsyncResult<TreatmentHistory[]>;
    satisfaction: AsyncResult<Satisfaction[]>;
    executionTime: number;
    cacheHitRate: number;
  }> {
    const startTime = Date.now();

    const [customer, appointments, treatmentHistory, satisfaction] = await Promise.all([
      this.fetchCustomerWithCache(customerId),
      this.fetchAppointmentsWithCache(customerId),
      this.fetchTreatmentHistoryWithCache(customerId),
      this.fetchSatisfactionWithCache(customerId)
    ]);

    const results = [customer, appointments, treatmentHistory, satisfaction];
    const cacheHits = results.filter(r => r.fromCache).length;
    const cacheHitRate = cacheHits / results.length;

    return {
      customer,
      appointments,
      treatmentHistory,
      satisfaction,
      executionTime: Date.now() - startTime,
      cacheHitRate
    };
  }

  /**
   * 예약 가능한 시간대를 병렬로 조회 (캐싱 적용)
   */
  async fetchAvailableTimeSlotsParallel(
    dates: string[],
    treatmentIds: UUID[]
  ): Promise<BatchResult<{ date: string; timeSlots: string[] }>> {
    const startTime = Date.now();

    const promises = dates.flatMap(date =>
      treatmentIds.map(treatmentId =>
        this.fetchAvailableTimeSlotsWithCache(date, treatmentId)
      )
    );

    const results = await Promise.all(promises);
    return this.createBatchResultWithCache(results, startTime);
  }

  /**
   * 리뷰와 만족도 데이터를 병렬로 조회 (캐싱 적용)
   */
  async fetchReviewsAndSatisfactionParallel(
    treatmentIds: UUID[]
  ): Promise<{
    reviews: BatchResult<Satisfaction[]>;
    averageRatings: BatchResult<number>;
    executionTime: number;
  }> {
    const startTime = Date.now();

    const [reviewsResult, ratingsResult] = await Promise.all([
      this.fetchReviewsForTreatmentsParallel(treatmentIds),
      this.fetchAverageRatingsParallel(treatmentIds)
    ]);

    return {
      reviews: reviewsResult,
      averageRatings: ratingsResult,
      executionTime: Date.now() - startTime
    };
  }

  // 캐싱 레이어가 적용된 메서드들
  private async fetchCustomerWithCache(customerId: UUID): Promise<AsyncResult<Customer>> {
    const cacheKey = `customer:${customerId}`;
    const cached = this.getFromCache<Customer>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchCustomerWithMetrics(customerId);
    if (result.success && result.data) {
      this.setCache(cacheKey, result.data, this.defaultTTL);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchAppointmentsWithCache(customerId: UUID): Promise<AsyncResult<Appointment[]>> {
    const cacheKey = `appointments:${customerId}`;
    const cached = this.getFromCache<Appointment[]>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchAppointmentsWithMetrics(customerId);
    if (result.success && result.data) {
      // 예약 데이터는 더 짧은 TTL (1분)
      this.setCache(cacheKey, result.data, 60000);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchTreatmentHistoryWithCache(customerId: UUID): Promise<AsyncResult<TreatmentHistory[]>> {
    const cacheKey = `treatment-history:${customerId}`;
    const cached = this.getFromCache<TreatmentHistory[]>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchTreatmentHistoryWithMetrics(customerId);
    if (result.success && result.data) {
      // 치료 이력은 더 긴 TTL (10분)
      this.setCache(cacheKey, result.data, 600000);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchSatisfactionWithCache(customerId: UUID): Promise<AsyncResult<Satisfaction[]>> {
    const cacheKey = `satisfaction:${customerId}`;
    const cached = this.getFromCache<Satisfaction[]>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchSatisfactionWithMetrics(customerId);
    if (result.success && result.data) {
      this.setCache(cacheKey, result.data, this.defaultTTL);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchTreatmentsByConcernWithCache(concern: string): Promise<AsyncResult<BeautyTreatment[]>> {
    const cacheKey = `treatments:concern:${concern}`;
    const cached = this.getFromCache<BeautyTreatment[]>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchTreatmentsByConcern(concern);
    if (result.success && result.data) {
      // 시술 정보는 긴 TTL (30분)
      this.setCache(cacheKey, result.data, 1800000);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchTreatmentsBySkinTypeWithCache(skinType: string): Promise<AsyncResult<BeautyTreatment[]>> {
    const cacheKey = `treatments:skin-type:${skinType}`;
    const cached = this.getFromCache<BeautyTreatment[]>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchTreatmentsBySkinType(skinType);
    if (result.success && result.data) {
      this.setCache(cacheKey, result.data, 1800000);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchAvailableTimeSlotsWithCache(
    date: string, 
    treatmentId: UUID
  ): Promise<AsyncResult<{ date: string; timeSlots: string[] }>> {
    const cacheKey = `time-slots:${date}:${treatmentId}`;
    const cached = this.getFromCache<{ date: string; timeSlots: string[] }>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchAvailableTimeSlotsForDateAndTreatment(date, treatmentId);
    if (result.success && result.data) {
      // 예약 가능 시간은 매우 짧은 TTL (30초)
      this.setCache(cacheKey, result.data, 30000);
    }
    
    return { ...result, fromCache: false };
  }

  // 캐시 관리 메서드들
  private getFromCache<T>(key: string): T | null {
    const item = this.cache.get(key);
    
    if (!item) {
      this.cacheStats.misses++;
      return null;
    }

    const now = Date.now();
    if (now - item.timestamp > item.ttl) {
      this.cache.delete(key);
      this.cacheStats.misses++;
      return null;
    }

    item.accessCount++;
    item.lastAccessed = now;
    this.cacheStats.hits++;
    
    return item.data;
  }

  private setCache<T>(key: string, data: T, ttl: number = this.defaultTTL): void {
    // 캐시 크기 제한 확인
    if (this.cache.size >= this.maxCacheSize) {
      this.evictLeastRecentlyUsed();
    }

    const now = Date.now();
    this.cache.set(key, {
      data,
      timestamp: now,
      ttl,
      accessCount: 1,
      lastAccessed: now
    });
  }

  private evictLeastRecentlyUsed(): void {
    let oldestKey: string | null = null;
    let oldestTime = Date.now();

    for (const [key, item] of this.cache.entries()) {
      if (item.lastAccessed < oldestTime) {
        oldestTime = item.lastAccessed;
        oldestKey = key;
      }
    }

    if (oldestKey) {
      this.cache.delete(oldestKey);
    }
  }

  private cleanupExpiredCache(): void {
    const now = Date.now();
    const keysToDelete: string[] = [];

    for (const [key, item] of this.cache.entries()) {
      if (now - item.timestamp > item.ttl) {
        keysToDelete.push(key);
      }
    }

    keysToDelete.forEach(key => this.cache.delete(key));
  }

  private updateCacheStats(): void {
    const total = this.cacheStats.hits + this.cacheStats.misses;
    this.cacheStats.hitRate = total > 0 ? this.cacheStats.hits / total : 0;
    this.cacheStats.totalSize = this.cache.size;
    
    // 대략적인 메모리 사용량 계산 (바이트)
    let memoryUsage = 0;
    for (const [key, item] of this.cache.entries()) {
      memoryUsage += key.length * 2; // UTF-16
      memoryUsage += JSON.stringify(item.data).length * 2;
      memoryUsage += 32; // 메타데이터 오버헤드
    }
    this.cacheStats.memoryUsage = memoryUsage;
  }

  private createBatchResultWithCache<T>(results: AsyncResult<T>[], startTime: number): BatchResult<T> {
    const cacheHits = results.filter(r => r.fromCache).length;
    const cacheHitRate = results.length > 0 ? cacheHits / results.length : 0;

    return {
      results,
      totalExecutionTime: Date.now() - startTime,
      successCount: results.filter(r => r.success).length,
      errorCount: results.filter(r => !r.success).length,
      cacheHitRate
    };
  }

  // Private helper methods
  private async fetchCustomerWithMetrics(customerId: UUID): Promise<AsyncResult<Customer>> {
    return this.executeWithMetrics(async () => {
      // Mock API call - 실제 구현에서는 실제 API 호출
      await this.delay(Math.random() * 1000);
      return {
        id: customerId,
        name: '김민지',
        phone: '+82-10-1234-5678',
        address: {
          street: '강남대로 123',
          city: '서울특별시',
          district: '강남구'
        },
        profile: {
          skinType: 'combination',
          concerns: ['주름', '색소침착'],
          previousTreatments: [],
          preferences: {
            language: 'ko',
            notificationMethods: ['email', 'sms']
          },
          tags: ['vip-customer']
        },
        createdAt: '2024-01-01T00:00:00Z',
        updatedAt: '2024-01-01T00:00:00Z'
      } as Customer;
    });
  }

  private async fetchAppointmentsWithMetrics(customerId: UUID): Promise<AsyncResult<Appointment[]>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 800);
      return [
        {
          id: 'apt-001',
          customerId,
          treatmentId: 'treatment-001',
          date: '2024-07-29',
          timeSlot: '14:00-16:00',
          duration: 120,
          status: 'confirmed',
          location: '엘리트 뷰티 클리닉 강남점',
          reminders: [],
          createdAt: '2024-01-01T00:00:00Z',
          updatedAt: '2024-01-01T00:00:00Z'
        }
      ] as Appointment[];
    });
  }

  private async fetchTreatmentHistoryWithMetrics(customerId: UUID): Promise<AsyncResult<TreatmentHistory[]>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 600);
      return [
        {
          id: 'history-001',
          treatmentId: 'treatment-001',
          treatmentName: '보톡스 (이마)',
          date: '2024-01-20T00:00:00Z',
          doctor: '김미용 원장',
          price: 350000,
          satisfaction: 5
        }
      ] as TreatmentHistory[];
    });
  }

  private async fetchSatisfactionWithMetrics(customerId: UUID): Promise<AsyncResult<Satisfaction[]>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 500);
      return [
        {
          id: 'satisfaction-001',
          customerId,
          appointmentId: 'apt-001',
          rating: 5,
          feedback: '매우 만족합니다',
          categories: {
            service: 5,
            cleanliness: 5,
            result: 5,
            value: 4
          },
          wouldRecommend: true,
          submittedAt: '2024-01-21T00:00:00Z'
        }
      ] as Satisfaction[];
    });
  }

  private async fetchTreatmentsByConcern(concern: string): Promise<AsyncResult<BeautyTreatment[]>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 400);
      return [
        {
          id: 'treatment-001',
          name: '보톡스 (이마)',
          category: 'botox',
          price: 200000,
          duration: 30,
          description: `${concern} 개선에 효과적인 시술`,
          tags: ['anti-aging', concern.toLowerCase()],
          isActive: true,
          createdAt: '2024-01-01T00:00:00Z',
          updatedAt: '2024-01-01T00:00:00Z'
        }
      ] as BeautyTreatment[];
    });
  }

  private async fetchTreatmentsBySkinType(skinType: string): Promise<AsyncResult<BeautyTreatment[]>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 400);
      return [
        {
          id: 'treatment-002',
          name: '히알루론산 필러',
          category: 'filler',
          price: 300000,
          duration: 45,
          description: `${skinType} 피부에 적합한 시술`,
          tags: ['hydration', skinType.toLowerCase()],
          isActive: true,
          createdAt: '2024-01-01T00:00:00Z',
          updatedAt: '2024-01-01T00:00:00Z'
        }
      ] as BeautyTreatment[];
    });
  }

  private async fetchAvailableTimeSlotsForDateAndTreatment(
    date: string, 
    treatmentId: UUID
  ): Promise<AsyncResult<{ date: string; timeSlots: string[] }>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 300);
      return {
        date,
        timeSlots: ['09:00-11:00', '14:00-16:00', '16:00-18:00']
      };
    });
  }

  private async fetchReviewsForTreatmentsParallel(treatmentIds: UUID[]): Promise<BatchResult<Satisfaction[]>> {
    const startTime = Date.now();
    const promises = treatmentIds.map(id => this.fetchReviewsForTreatmentWithCache(id));
    const results = await Promise.all(promises);
    return this.createBatchResult(results, startTime);
  }

  private async fetchAverageRatingsParallel(treatmentIds: UUID[]): Promise<BatchResult<number>> {
    const startTime = Date.now();
    const promises = treatmentIds.map(id => this.fetchAverageRatingForTreatmentWithCache(id));
    const results = await Promise.all(promises);
    return this.createBatchResult(results, startTime);
  }

  private async fetchReviewsForTreatmentWithCache(treatmentId: UUID): Promise<AsyncResult<Satisfaction[]>> {
    const cacheKey = `reviews:${treatmentId}`;
    const cached = this.getFromCache<Satisfaction[]>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchReviewsForTreatment(treatmentId);
    if (result.success && result.data) {
      // 리뷰는 중간 TTL (10분)
      this.setCache(cacheKey, result.data, 600000);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchAverageRatingForTreatmentWithCache(treatmentId: UUID): Promise<AsyncResult<number>> {
    const cacheKey = `rating:${treatmentId}`;
    const cached = this.getFromCache<number>(cacheKey);
    
    if (cached) {
      return {
        success: true,
        data: cached,
        executionTime: 0,
        fromCache: true
      };
    }

    const result = await this.fetchAverageRatingForTreatment(treatmentId);
    if (result.success && result.data !== undefined) {
      // 평균 평점은 중간 TTL (10분)
      this.setCache(cacheKey, result.data, 600000);
    }
    
    return { ...result, fromCache: false };
  }

  private async fetchReviewsForTreatment(treatmentId: UUID): Promise<AsyncResult<Satisfaction[]>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 200);
      return [] as Satisfaction[]; // Mock empty array
    });
  }

  private async fetchAverageRatingForTreatment(treatmentId: UUID): Promise<AsyncResult<number>> {
    return this.executeWithMetrics(async () => {
      await this.delay(Math.random() * 150);
      return 4.5 + Math.random() * 0.5; // Mock rating 4.5-5.0
    });
  }

  private async executeWithMetrics<T>(operation: () => Promise<T>): Promise<AsyncResult<T>> {
    const startTime = Date.now();
    try {
      const data = await Promise.race([
        operation(),
        this.createTimeoutPromise<T>()
      ]);
      
      return {
        success: true,
        data,
        executionTime: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        executionTime: Date.now() - startTime
      };
    }
  }

  private handleSettledResult<T>(
    result: PromiseSettledResult<AsyncResult<T>>, 
    identifier: string
  ): AsyncResult<T> {
    if (result.status === 'fulfilled') {
      return result.value;
    } else {
      return {
        success: false,
        error: `${identifier}: ${result.reason}`,
        executionTime: 0
      };
    }
  }

  private createBatchResult<T>(results: AsyncResult<T>[], startTime: number): BatchResult<T> {
    const cacheHits = results.filter(r => r.fromCache).length;
    const cacheHitRate = results.length > 0 ? cacheHits / results.length : 0;

    return {
      results,
      totalExecutionTime: Date.now() - startTime,
      successCount: results.filter(r => r.success).length,
      errorCount: results.filter(r => !r.success).length,
      cacheHitRate
    };
  }

  private createBatches<T>(items: T[], batchSize: number): T[][] {
    const batches: T[][] = [];
    for (let i = 0; i < items.length; i += batchSize) {
      batches.push(items.slice(i, i + batchSize));
    }
    return batches;
  }

  private createTimeoutPromise<T>(): Promise<T> {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Operation timeout')), this.timeout);
    });
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 싱글톤 인스턴스
export const asyncOptimizer = new AsyncOptimizer();

export default AsyncOptimizer; 