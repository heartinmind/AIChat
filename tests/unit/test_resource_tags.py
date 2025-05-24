"""Resource tags unit tests for beauty clinic chatbot."""

import pytest
from unittest.mock import Mock, patch
from customer_service.tools.tools import (
    access_cart_information,
    get_product_recommendations,
    schedule_planting_service
)


class TestResourceTags:
    """Test resource tagging and categorization in beauty clinic chatbot."""
    
    def test_beauty_treatment_categorization(self):
        """Test that beauty treatments are properly categorized."""
        # Test botox treatment
        result = get_product_recommendations("주름", "123")
        assert "보톡스" in str(result)
        assert "이마" in str(result)
        
        # Test pigmentation treatment
        result = get_product_recommendations("색소침착", "123")
        assert "레이저" in str(result)
        assert "피코" in str(result)
    
    def test_cart_information_structure(self):
        """Test that cart information has proper structure and tags."""
        result = access_cart_information("123")
        
        # Check required fields
        assert "items" in result
        assert "subtotal" in result
        
        # Check item structure
        if result["items"]:
            item = result["items"][0]
            assert "product_id" in item
            assert "name" in item
            assert "quantity" in item
            assert "price" in item
    
    def test_appointment_scheduling_tags(self):
        """Test appointment scheduling includes proper metadata tags."""
        result = schedule_planting_service(
            customer_id="123",
            date="2024-07-29", 
            time_range="9-12",
            details="보톡스 이마 시술"
        )
        
        # Check response structure
        assert result["status"] == "success"
        assert "appointment_id" in result
        assert "location" in result
        assert "엘리트 뷰티 클리닉" in result["location"]
    
    def test_korean_language_tags(self):
        """Test that Korean language content is properly tagged."""
        # Test Korean treatment names
        result = get_product_recommendations("주름", "123")
        recommendations = result.get("recommendations", [])
        
        for rec in recommendations:
            assert "name" in rec
            # Ensure Korean characters are preserved
            korean_name = rec["name"]
            assert any(ord(char) >= 0xAC00 and ord(char) <= 0xD7AF for char in korean_name)
    
    @patch('customer_service.tools.tools.logger')
    def test_logging_tags(self, mock_logger):
        """Test that proper logging tags are applied."""
        access_cart_information("test_customer")
        
        # Verify logging was called with customer ID
        mock_logger.info.assert_called()
        call_args = mock_logger.info.call_args[0]
        assert "test_customer" in str(call_args)
    
    def test_treatment_price_tags(self):
        """Test that treatment prices are properly tagged."""
        result = get_product_recommendations("주름", "123")
        recommendations = result.get("recommendations", [])
        
        for rec in recommendations:
            assert "price" in rec
            assert isinstance(rec["price"], int)
            assert rec["price"] > 0


class TestBeautyClinicMetadata:
    """Test metadata and tagging for beauty clinic specific features."""
    
    def test_customer_profile_tags(self):
        """Test customer profile contains proper metadata tags."""
        # This would test customer.py functionality
        # Add tests for BeautyProfile fields like skin_type, concerns, etc.
        pass
    
    def test_notification_tags(self):
        """Test notification system uses proper categorization."""
        # This would test notification tools
        # Add tests for send_appointment_reminder, etc.
        pass
    
    def test_mobile_integration_tags(self):
        """Test mobile integration features have proper tags."""
        # This would test mobile app related tools
        # Add tests for generate_mobile_deep_link, etc.
        pass


if __name__ == "__main__":
    pytest.main([__file__]) 