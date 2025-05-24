/**
 * Resource Tags Unit Tests
 * Tests for beauty clinic chatbot resource tagging and categorization
 */

// Jest 기본 함수들 (전역에서 사용 가능)
declare const describe: (name: string, fn: () => void) => void;
declare const it: (name: string, fn: () => void) => void;
declare const expect: (value: any) => any;
declare const beforeEach: (fn: () => void) => void;

// 타입 정의 import
import type {
  BeautyTreatment,
  CustomerProfile,
  Appointment,
  TreatmentCategory,
  SkinType,
  SkinConcern,
  AppointmentStatus
} from '../types';

// Mock types for testing
interface TestBeautyTreatment extends BeautyTreatment {
  // 테스트용 추가 필드
}

interface TestCustomerProfile extends CustomerProfile {
  // 테스트용 추가 필드  
}

interface TestAppointmentData extends Appointment {
  // 테스트용 추가 필드
  tags: string[];
}

// Mock data
const mockTreatments: TestBeautyTreatment[] = [
  {
    id: 'botox-001',
    name: '보톡스 (이마)',
    category: 'botox',
    price: 200000,
    duration: 30,
    description: '이마 주름 개선 시술',
    tags: ['wrinkle-treatment', 'forehead', 'korean'],
    isActive: true,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z'
  },
  {
    id: 'filler-001', 
    name: '히알루론산 필러',
    category: 'filler',
    price: 300000,
    duration: 45,
    description: '볼륨 개선 및 주름 완화',
    tags: ['volume-enhancement', 'hyaluronic-acid', 'korean'],
    isActive: true,
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-01T00:00:00Z'
  }
];

const mockCustomer: TestCustomerProfile = {
  skinType: 'combination',
  concerns: ['색소침착', '주름', '모공'],
  previousTreatments: [],
  preferences: {
    language: 'ko',
    notificationMethods: ['email', 'sms'],
    notes: 'VIP 고객'
  },
  tags: ['vip-customer', 'korean-speaker', 'gangnam-location']
};

describe('Resource Tags', () => {
  describe('Treatment Categorization', () => {
    it('should properly categorize botox treatments', () => {
      const botoxTreatments = mockTreatments.filter(t => t.category === 'botox');
      
      expect(botoxTreatments).toHaveLength(1);
      expect(botoxTreatments[0].tags).toContain('wrinkle-treatment');
      expect(botoxTreatments[0].name).toMatch(/보톡스/);
    });

    it('should include Korean language tags', () => {
      mockTreatments.forEach(treatment => {
        expect(treatment.tags).toContain('korean');
        expect(/[가-힣]/.test(treatment.name)).toBe(true);
      });
    });

    it('should have proper price and duration tags', () => {
      mockTreatments.forEach(treatment => {
        expect(treatment.price).toBeGreaterThan(0);
        expect(treatment.duration).toBeGreaterThan(0);
        expect(typeof treatment.price).toBe('number');
      });
    });

    it('should have required metadata fields', () => {
      mockTreatments.forEach(treatment => {
        expect(treatment.id).toBeDefined();
        expect(treatment.name).toBeDefined();
        expect(treatment.category).toBeDefined();
        expect(treatment.isActive).toBeDefined();
        expect(treatment.createdAt).toBeDefined();
        expect(treatment.updatedAt).toBeDefined();
      });
    });
  });

  describe('Customer Profile Tags', () => {
    it('should tag customers with proper attributes', () => {
      expect(mockCustomer.tags).toContain('korean-speaker');
      expect(mockCustomer.tags).toContain('gangnam-location');
      expect(mockCustomer.skinType).toBe('combination');
    });

    it('should properly categorize skin concerns', () => {
      const koreanConcerns: SkinConcern[] = ['색소침착', '주름', '모공'];
      expect(mockCustomer.concerns).toEqual(koreanConcerns);
      
      mockCustomer.concerns.forEach(concern => {
        expect(/[가-힣]/.test(concern)).toBe(true);
      });
    });

    it('should validate notification preferences', () => {
      expect(mockCustomer.preferences.language).toBe('ko');
      expect(mockCustomer.preferences.notificationMethods).toContain('email');
      expect(mockCustomer.preferences.notificationMethods).toContain('sms');
    });
  });

  describe('Appointment Resource Tags', () => {
    let mockAppointment: TestAppointmentData;

    beforeEach(() => {
      mockAppointment = {
        id: 'apt-001',
        customerId: 'cust-123',
        treatmentId: 'botox-001',
        date: '2024-07-29',
        timeSlot: '09:00-12:00',
        duration: 180,
        status: 'confirmed',
        location: '엘리트 뷰티 클리닉 강남점',
        reminders: [],
        createdAt: '2024-01-01T00:00:00Z',
        updatedAt: '2024-01-01T00:00:00Z',
        tags: ['beauty-clinic', 'gangnam', 'korean-service']
      };
    });

    it('should include location and language tags', () => {
      expect(mockAppointment.tags).toContain('gangnam');
      expect(mockAppointment.tags).toContain('korean-service');
    });

    it('should have proper status categorization', () => {
      const validStatuses: AppointmentStatus[] = ['confirmed', 'pending', 'cancelled', 'completed', 'no-show'];
      expect(validStatuses).toContain(mockAppointment.status);
    });

    it('should include Korean location text', () => {
      expect(/[가-힣]/.test(mockAppointment.location)).toBe(true);
      expect(mockAppointment.location).toContain('엘리트 뷰티 클리닉');
    });
  });

  describe('Data Validation and Tagging', () => {
    it('should validate Korean text encoding', () => {
      const koreanText = '엘리트 뷰티 클리닉';
      const hasKoreanChars = /[가-힣]/.test(koreanText);
      
      expect(hasKoreanChars).toBe(true);
      expect(koreanText.length).toBeGreaterThan(0);
    });

    it('should ensure consistent tag formatting', () => {
      const allTags = [
        ...mockTreatments.flatMap(t => t.tags),
        ...mockCustomer.tags
      ];

      allTags.forEach(tag => {
        expect(tag).toMatch(/^[a-z-]+$/); // lowercase with hyphens
        expect(tag).not.toContain(' '); // no spaces
      });
    });

    it('should maintain referential integrity', () => {
      // Test that customer ID references are valid
      expect('cust-123').toMatch(/^cust-\d+$/);
      
      // Test that treatment IDs follow pattern
      mockTreatments.forEach(treatment => {
        expect(treatment.id).toMatch(/^[a-z]+-\d+$/);
      });
    });

    it('should validate price formatting', () => {
      mockTreatments.forEach(treatment => {
        expect(treatment.price).toBeGreaterThan(0);
        expect(Number.isInteger(treatment.price)).toBe(true);
        // Korean Won formatting test
        const formatted = treatment.price.toLocaleString('ko-KR');
        expect(formatted).toBeDefined();
      });
    });
  });

  describe('Search and Filter Tags', () => {
    it('should support filtering by treatment category', () => {
      const botoxTreatments = mockTreatments.filter(
        t => t.category === 'botox'
      );
      const fillerTreatments = mockTreatments.filter(
        t => t.category === 'filler'  
      );

      expect(botoxTreatments.length).toBeGreaterThan(0);
      expect(fillerTreatments.length).toBeGreaterThan(0);
    });

    it('should support search by Korean keywords', () => {
      const wrinkleTreatments = mockTreatments.filter(
        t => t.name.includes('보톡스') || t.tags.includes('wrinkle-treatment')
      );

      expect(wrinkleTreatments.length).toBeGreaterThan(0);
    });

    it('should support price range filtering', () => {
      const expensiveTreatments = mockTreatments.filter(
        t => t.price > 250000
      );
      const affordableTreatments = mockTreatments.filter(
        t => t.price <= 250000
      );

      expect(expensiveTreatments.length + affordableTreatments.length)
        .toBe(mockTreatments.length);
    });

    it('should support duration-based filtering', () => {
      const shortTreatments = mockTreatments.filter(
        t => t.duration <= 30
      );
      const longTreatments = mockTreatments.filter(
        t => t.duration > 30
      );

      expect(shortTreatments.length + longTreatments.length)
        .toBe(mockTreatments.length);
    });
  });
});

export {
  TestBeautyTreatment,
  TestCustomerProfile,
  TestAppointmentData
}; 
