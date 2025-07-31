import pytest
#from lib.Utils import get_spark_session
from lib.DataReader import read_customers, read_orders
from lib.DataManipulation import filter_closed_orders, count_orders_state, filter_orders_generic
from lib.ConfigReader import get_app_config

#fixture is used to set up code
#@pytest.fixture
#def spark():
 
@pytest.mark.skip()   #return get_spark_session("LOCAL")
def test_read_customers_df(spark): 
    #spark = get_spark_session("LOCAL")  #here we removed get_spark_session("LOCAL") because calling fixture
    customers_df_count = read_customers(spark, "LOCAL").count()   #read_customers(spark_session_name, env_name)4
    assert customers_df_count == 12435     #is used to check this number is equal or not

#all below test cases using regular methods not fixtures, we used fixture only one test case
#if we want to use fixture just replace (spark) in test_case_name
@pytest.mark.skip()
def test_read_orders_data(spark):
    orders_df_count = read_orders(spark, "LOCAL").count()
    assert orders_df_count == 68884
@pytest.mark.skip("work in progress")
def test_filter_closed_orders(spark):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_closed_orders(orders_df).count()
    assert filtered_count == 7556
@pytest.mark.skip()
def test_read_app_configs():
    config = get_app_config("LOCAL")
    assert config["orders.file.path"] == "data/orders.csv"

@pytest.mark.skip()    
def test_count_orders_state(spark, expected_results):
    customers_df = read_customers(spark, "LOCAL")
    actual_results = count_orders_state(customers_df)
    assert actual_results.collect() == expected_results.collect()
@pytest.mark.skip()
def test_check_closed_count(spark):
    orders_df = read_orders(spark, "LOCAL")
    filter_count = filter_orders_generic(orders_df, "CLOSED").count()
    assert filter_count == 7556
@pytest.mark.skip()
def test_check_complete_count(spark):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_orders_generic(orders_df, "COMPLETE").count()
    assert filtered_count == 22900
@pytest.mark.skip()
def test_check_pending_count(spark):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_orders_generic(orders_df, "PENDING_PAYMENT").count()
    assert filtered_count == 15030
@pytest.mark.parametrize(
    "status, count",[
        ("CLOSED", 7556),
        ("PENDING_PAYMENT", 15030),
        ("COMPLETE",22900)
    ]
)
def test_check_count(spark, status, count):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_orders_generic(orders_df, status).count()
    assert filtered_count == count 