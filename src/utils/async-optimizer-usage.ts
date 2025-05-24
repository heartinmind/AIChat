// Copyright 2025 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * AsyncOptimizer 사용 예제 및 성능 모니터링
 * Usage examples and performance monitoring for AsyncOptimizer
 */

import { AsyncOptimizer } from './async-optimizer';
import type { UUID } from '../types';

// 캐싱이 적용된 옵티마이저 인스턴스 생성
const optimizer = new AsyncOptimizer(
  10,       // maxConcurrency
  30000,    // timeout
  300000,   // defaultTTL (5분)
  1000      // maxCacheSize
);

/**
 * 고객 데이터 조회 성능 테스트
 */
export async function performanceTest() {
  const customerId: UUID = 'customer-123';
  
  console.log('=== 캐시 성능 테스트 시작 ===');
  
  // 첫 번째 호출 (캐시 없음)
  console.log('\n1. 첫 번째 호출 (캐시 미스):');
  const firstCall = await optimizer.fetchCustomerCompleteData(customerId);
  console.log(`실행 시간: ${firstCall.executionTime}ms`);
  console.log(`캐시 히트율: ${(firstCall.cacheHitRate * 100).toFixed(2)}%`);
  
  // 두 번째 호출 (캐시 적중)
  console.log('\n2. 두 번째 호출 (캐시 히트):');
  const secondCall = await optimizer.fetchCustomerCompleteData(customerId);
  console.log(`실행 시간: ${secondCall.executionTime}ms`);
  console.log(`캐시 히트율: ${(secondCall.cacheHitRate * 100).toFixed(2)}%`);
  
  // 캐시 통계 확인
  const stats = optimizer.getCacheStats();
  console.log('\n3. 현재 캐시 통계:');
  console.log(`총 히트: ${stats.hits}`);
  console.log(`총 미스: ${stats.misses}`);
  console.log(`전체 히트율: ${(stats.hitRate * 100).toFixed(2)}%`);
  console.log(`캐시 크기: ${stats.totalSize}개`);
  console.log(`메모리 사용량: ${(stats.memoryUsage / 1024).toFixed(2)}KB`);
}

/**
 * 배치 처리 성능 테스트
 */
export async function batchPerformanceTest() {
  const customerIds: UUID[] = [
    'customer-001', 'customer-002', 'customer-003', 
    'customer-004', 'customer-005'
  ];
  
  console.log('\n=== 배치 처리 성능 테스트 ===');
  
  // 첫 번째 배치 호출
  console.log('\n1. 첫 번째 배치 호출:');
  const firstBatch = await optimizer.fetchCustomersParallel(customerIds);
  console.log(`총 실행 시간: ${firstBatch.totalExecutionTime}ms`);
  console.log(`성공: ${firstBatch.successCount}, 실패: ${firstBatch.errorCount}`);
  console.log(`캐시 히트율: ${(firstBatch.cacheHitRate * 100).toFixed(2)}%`);
  
  // 두 번째 배치 호출 (같은 고객들)
  console.log('\n2. 두 번째 배치 호출 (캐시 적중):');
  const secondBatch = await optimizer.fetchCustomersParallel(customerIds);
  console.log(`총 실행 시간: ${secondBatch.totalExecutionTime}ms`);
  console.log(`성공: ${secondBatch.successCount}, 실패: ${secondBatch.errorCount}`);
  console.log(`캐시 히트율: ${(secondBatch.cacheHitRate * 100).toFixed(2)}%`);
  
  console.log(`\n성능 향상: ${Math.round((firstBatch.totalExecutionTime / secondBatch.totalExecutionTime) * 100) / 100}배 빨라짐`);
}

/**
 * 시술 추천 성능 테스트
 */
export async function treatmentRecommendationTest() {
  const concerns = ['주름', '색소침착', '탄력저하'];
  const skinTypes = ['지성', '건성', '복합성'];
  
  console.log('\n=== 시술 추천 성능 테스트 ===');
  
  // 첫 번째 호출
  console.log('\n1. 첫 번째 호출:');
  const start1 = Date.now();
  const first = await optimizer.fetchTreatmentRecommendationsParallel(concerns, skinTypes);
  const time1 = Date.now() - start1;
  console.log(`실행 시간: ${time1}ms`);
  console.log(`캐시 히트율: ${(first.cacheHitRate * 100).toFixed(2)}%`);
  
  // 두 번째 호출 (캐시 적중)
  console.log('\n2. 두 번째 호출:');
  const start2 = Date.now();
  const second = await optimizer.fetchTreatmentRecommendationsParallel(concerns, skinTypes);
  const time2 = Date.now() - start2;
  console.log(`실행 시간: ${time2}ms`);
  console.log(`캐시 히트율: ${(second.cacheHitRate * 100).toFixed(2)}%`);
}

/**
 * 캐시 메모리 사용량 모니터링
 */
export function monitorCacheUsage() {
  console.log('\n=== 캐시 메모리 모니터링 시작 ===');
  
  const interval = setInterval(() => {
    const stats = optimizer.getCacheStats();
    console.log(`[${new Date().toLocaleTimeString()}] 캐시 상태:`);
    console.log(`  - 크기: ${stats.totalSize}개`);
    console.log(`  - 메모리: ${(stats.memoryUsage / 1024).toFixed(2)}KB`);
    console.log(`  - 히트율: ${(stats.hitRate * 100).toFixed(2)}%`);
    console.log(`  - 총 히트: ${stats.hits}, 총 미스: ${stats.misses}`);
    
    // 메모리 사용량이 1MB를 초과하면 경고
    if (stats.memoryUsage > 1024 * 1024) {
      console.warn('⚠️ 캐시 메모리 사용량이 1MB를 초과했습니다!');
    }
    
    // 히트율이 50% 미만이면 경고
    if (stats.hitRate < 0.5 && stats.hits + stats.misses > 10) {
      console.warn('⚠️ 캐시 히트율이 50% 미만입니다. 캐시 전략을 검토해보세요.');
    }
  }, 10000); // 10초마다 모니터링
  
  // 1분 후 모니터링 중지
  setTimeout(() => {
    clearInterval(interval);
    console.log('캐시 모니터링이 종료되었습니다.');
  }, 60000);
}

/**
 * 캐시 효과 비교 테스트
 */
export async function cacheEffectComparison() {
  console.log('\n=== 캐시 효과 비교 테스트 ===');
  
  // 캐시 초기화
  optimizer.clearCache();
  
  const testData = {
    customerIds: ['customer-001', 'customer-002', 'customer-003'],
    concerns: ['주름', '색소침착'],
    skinTypes: ['지성', '건성']
  };
  
  // 10번 반복 테스트
  const results = [];
  
  for (let i = 0; i < 10; i++) {
    const start = Date.now();
    
    // 여러 작업을 병렬로 실행
    await Promise.all([
      optimizer.fetchCustomersParallel(testData.customerIds),
      optimizer.fetchTreatmentRecommendationsParallel(testData.concerns, testData.skinTypes),
      ...testData.customerIds.map(id => optimizer.fetchCustomerCompleteData(id))
    ]);
    
    const executionTime = Date.now() - start;
    const stats = optimizer.getCacheStats();
    
    results.push({
      iteration: i + 1,
      executionTime,
      hitRate: stats.hitRate,
      cacheSize: stats.totalSize
    });
    
    console.log(`반복 ${i + 1}: ${executionTime}ms, 히트율: ${(stats.hitRate * 100).toFixed(2)}%`);
  }
  
  // 결과 분석
  const avgExecutionTime = results.reduce((sum, r) => sum + r.executionTime, 0) / results.length;
  const finalHitRate = results[results.length - 1].hitRate;
  const firstCallTime = results[0].executionTime;
  const lastCallTime = results[results.length - 1].executionTime;
  
  console.log('\n📊 테스트 결과 요약:');
  console.log(`평균 실행 시간: ${avgExecutionTime.toFixed(2)}ms`);
  console.log(`최종 캐시 히트율: ${(finalHitRate * 100).toFixed(2)}%`);
  console.log(`첫 번째 vs 마지막 호출: ${firstCallTime}ms → ${lastCallTime}ms`);
  console.log(`성능 향상: ${((firstCallTime / lastCallTime) * 100 - 100).toFixed(2)}%`);
}

/**
 * TTL 테스트 (캐시 만료 확인)
 */
export async function ttlTest() {
  console.log('\n=== TTL 테스트 (캐시 만료 확인) ===');
  
  // 짧은 TTL로 새 옵티마이저 생성 (테스트용)
  const shortTTLOptimizer = new AsyncOptimizer(10, 30000, 2000); // 2초 TTL
  
  const customerId: UUID = 'customer-ttl-test';
  
  // 첫 번째 호출
  console.log('1. 첫 번째 호출:');
  const first = await shortTTLOptimizer.fetchCustomerCompleteData(customerId);
  console.log(`캐시 히트율: ${(first.cacheHitRate * 100).toFixed(2)}%`);
  
  // 즉시 두 번째 호출 (캐시 적중)
  console.log('2. 즉시 두 번째 호출:');
  const second = await shortTTLOptimizer.fetchCustomerCompleteData(customerId);
  console.log(`캐시 히트율: ${(second.cacheHitRate * 100).toFixed(2)}%`);
  
  // 3초 대기 후 호출 (캐시 만료)
  console.log('3. 3초 대기 후 호출 (캐시 만료 예상):');
  await new Promise(resolve => setTimeout(resolve, 3000));
  const third = await shortTTLOptimizer.fetchCustomerCompleteData(customerId);
  console.log(`캐시 히트율: ${(third.cacheHitRate * 100).toFixed(2)}%`);
  
  const stats = shortTTLOptimizer.getCacheStats();
  console.log(`\n최종 통계: 히트 ${stats.hits}, 미스 ${stats.misses}`);
}

// 모든 테스트 실행
export async function runAllTests() {
  console.log('🚀 AsyncOptimizer 캐싱 성능 테스트 시작\n');
  
  try {
    await performanceTest();
    await batchPerformanceTest();
    await treatmentRecommendationTest();
    await cacheEffectComparison();
    await ttlTest();
    
    console.log('\n✅ 모든 테스트가 완료되었습니다!');
    
    // 최종 캐시 상태
    const finalStats = optimizer.getCacheStats();
    console.log('\n📈 최종 캐시 통계:');
    console.log(`총 캐시 항목: ${finalStats.totalSize}개`);
    console.log(`총 메모리 사용량: ${(finalStats.memoryUsage / 1024).toFixed(2)}KB`);
    console.log(`전체 히트율: ${(finalStats.hitRate * 100).toFixed(2)}%`);
    console.log(`총 히트: ${finalStats.hits}, 총 미스: ${finalStats.misses}`);
    
  } catch (error) {
    console.error('❌ 테스트 중 오류 발생:', error);
  }
}

// 개발 환경에서 바로 테스트 실행
if (process.env.NODE_ENV === 'development') {
  runAllTests();
} 
