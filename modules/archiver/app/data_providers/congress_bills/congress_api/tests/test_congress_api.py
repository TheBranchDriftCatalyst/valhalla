import pytest
from app.data_providers.congress_bills.congress_api.congress_api import CongressAPI
import pytest_vcr

# @pytest.mark.vcr()
def test_get_bills_with_recent_updates():
    api = CongressAPI(default_params={"limit": "1"})
    response = api.get_bill()
    
    api.follow_link(response['bills'][0]['url'])
    assert response.status_code == 200

# Continue to create similar tests for other methods
