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
 * 캐시 디버깅 및 테스트 파일
 * Cache debugging and testing file
 */

import { AsyncOptimizer } from './async-optimizer';
import type { UUID } from '../types';

async function debugCacheIssue() {
  console.log('🔍 캐시 디버깅 시작...\n');

  // 새로운 옵티마이저 인스턴스 생성 (작은 TTL로 테스트)
  const optimizer = new AsyncOptimizer(
    5,     // maxConcurrency
    10000, // timeout
    5000,  // TTL: 5초
    100    // maxCacheSize
  );

  const customerId: UUID = 'debug-customer-123';

  console.log('=== 첫 번째 호출 (캐시 미스 예상) ===');
  const start1 = Date.now();
  const result1 = await optimizer.fetchCustomerCompleteData(customerId);
  const time1 = Date.now() - start1;
  
  console.log(`실행 시간: ${time1}ms`);
  console.log(`캐시 히트율: ${(result1.cacheHitRate * 100).toFixed(2)}%`);
  console.log('개별 결과 분석:');
  console.log(`- Customer: fromCache=${result1.customer.fromCache}, executionTime=${result1.customer.executionTime}ms`);
  console.log(`- Appointments: fromCache=${result1.appointments.fromCache}, executionTime=${result1.appointments.executionTime}ms`);
  console.log(`- TreatmentHistory: fromCache=${result1.treatmentHistory.fromCache}, executionTime=${result1.treatmentHistory.executionTime}ms`);
  console.log(`- Satisfaction: fromCache=${result1.satisfaction.fromCache}, executionTime=${result1.satisfaction.executionTime}ms`);

  // 캐시 상태 확인
  const stats1 = optimizer.getCacheStats();
  console.log(`\n캐시 상태: 히트=${stats1.hits}, 미스=${stats1.misses}, 크기=${stats1.totalSize}`);

  console.log('\n=== 즉시 두 번째 호출 (캐시 히트 예상) ===');
  const start2 = Date.now();
  const result2 = await optimizer.fetchCustomerCompleteData(customerId);
  const time2 = Date.now() - start2;
  
  console.log(`실행 시간: ${time2}ms`);
  console.log(`캐시 히트율: ${(result2.cacheHitRate * 100).toFixed(2)}%`);
  console.log('개별 결과 분석:');
  console.log(`- Customer: fromCache=${result2.customer.fromCache}, executionTime=${result2.customer.executionTime}ms`);
  console.log(`- Appointments: fromCache=${result2.appointments.fromCache}, executionTime=${result2.appointments.executionTime}ms`);
  console.log(`- TreatmentHistory: fromCache=${result2.treatmentHistory.fromCache}, executionTime=${result2.treatmentHistory.executionTime}ms`);
  console.log(`- Satisfaction: fromCache=${result2.satisfaction.fromCache}, executionTime=${result2.satisfaction.executionTime}ms`);

  // 캐시 상태 확인
  const stats2 = optimizer.getCacheStats();
  console.log(`\n캐시 상태: 히트=${stats2.hits}, 미스=${stats2.misses}, 크기=${stats2.totalSize}`);

  console.log('\n=== 6초 대기 후 세 번째 호출 (TTL 만료로 캐시 미스 예상) ===');
  await new Promise(resolve => setTimeout(resolve, 6000));
  
  const start3 = Date.now();
  const result3 = await optimizer.fetchCustomerCompleteData(customerId);
  const time3 = Date.now() - start3;
  
  console.log(`실행 시간: ${time3}ms`);
  console.log(`캐시 히트율: ${(result3.cacheHitRate * 100).toFixed(2)}%`);
  console.log('개별 결과 분석:');
  console.log(`- Customer: fromCache=${result3.customer.fromCache}, executionTime=${result3.customer.executionTime}ms`);
  console.log(`- Appointments: fromCache=${result3.appointments.fromCache}, executionTime=${result3.appointments.executionTime}ms`);
  console.log(`- TreatmentHistory: fromCache=${result3.treatmentHistory.fromCache}, executionTime=${result3.treatmentHistory.executionTime}ms`);
  console.log(`- Satisfaction: fromCache=${result3.satisfaction.fromCache}, executionTime=${result3.satisfaction.executionTime}ms`);

  // 최종 캐시 상태
  const finalStats = optimizer.getCacheStats();
  console.log(`\n최종 캐시 상태: 히트=${finalStats.hits}, 미스=${finalStats.misses}, 크기=${finalStats.totalSize}`);
  
  console.log('\n📊 성능 비교:');
  console.log(`첫 번째 호출: ${time1}ms`);
  console.log(`두 번째 호출: ${time2}ms (개선율: ${((time1 - time2) / time1 * 100).toFixed(2)}%)`);
  console.log(`세 번째 호출: ${time3}ms`);

  // 캐시가 정상 작동하는지 판단
  if (result2.cacheHitRate > 0.5 && time2 < time1 * 0.1) {
    console.log('\n✅ 캐시가 정상적으로 작동하고 있습니다!');
  } else {
    console.log('\n❌ 캐시가 제대로 작동하지 않습니다.');
    console.log('가능한 원인:');
    console.log('1. fromCache 플래그가 제대로 설정되지 않음');
    console.log('2. TTL이 너무 짧음');
    console.log('3. 캐시 키가 제대로 생성되지 않음');
    console.log('4. 캐시 데이터가 제대로 저장되지 않음');
  }
}

// 간단한 캐시 테스트
async function simpleCacheTest() {
  console.log('\n🧪 간단한 캐시 기능 테스트...\n');
  
  const optimizer = new AsyncOptimizer(5, 10000, 10000, 100); // 10초 TTL
  
  // 단일 고객 조회 테스트
  const customerId: UUID = 'simple-test-customer';
  
  console.log('첫 번째 고객 조회...');
  const start1 = Date.now();
  const customer1 = await optimizer.fetchCustomersParallel([customerId]);
  const time1 = Date.now() - start1;
  console.log(`시간: ${time1}ms, 캐시 히트율: ${(customer1.cacheHitRate * 100).toFixed(2)}%`);

  console.log('두 번째 고객 조회 (캐시 적중 예상)...');
  const start2 = Date.now();
  const customer2 = await optimizer.fetchCustomersParallel([customerId]);
  const time2 = Date.now() - start2;
  console.log(`시간: ${time2}ms, 캐시 히트율: ${(customer2.cacheHitRate * 100).toFixed(2)}%`);

  console.log(`\n개선율: ${((time1 - time2) / time1 * 100).toFixed(2)}%`);
  
  const stats = optimizer.getCacheStats();
  console.log(`캐시 통계: 히트=${stats.hits}, 미스=${stats.misses}, 히트율=${(stats.hitRate * 100).toFixed(2)}%`);
}

// 실행
async function runDebugTests() {
  try {
    await debugCacheIssue();
    await simpleCacheTest();
  } catch (error) {
    console.error('디버깅 중 오류 발생:', error);
  }
}

if (require.main === module) {
  runDebugTests();
}

export { debugCacheIssue, simpleCacheTest, runDebugTests }; 
