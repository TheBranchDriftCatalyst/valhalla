import pytest
import pytest_vcr

from app.data_providers.congress_gov.api.endpoints.bill_api import BillApi

congress_api = BillApi(default_params={"limit": "1"})

# @pytest.mark.vcr()
def test_get_bills_with_recent_updates():
    response = congress_api.get_bill()
    assert len(response['bills']) == 1
    assert response['bills'][0]['url'] == 'https://api.congress.gov/v3/bill/118/hr/4495?format=json'
    

# @pytest.mark.vcr()
def test_get_bill():
    response = congress_api.get_bill(congress=117, bill_type='hr', bill_number=3076)
    assert response['bill'] is not None

# Continue to create similar tests for other methods
