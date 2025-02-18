from prefect import task
import great_expectations as gx
import pandas as pd

@task
def validate_data(data):
    context = gx.get_context()

    # Add a pandas data source if not already present
    data_source = context.data_sources.add_pandas("pandas")
    data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")

    # Define batch for the entire dataframe
    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch definition")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": data})

    # Create an expectation suite
    suite = context.suites.add(
        gx.core.expectation_suite.ExpectationSuite(name="expectations")
    )

    # Updated expectations list
    expectations = [
        gx.expectations.ExpectColumnValuesToBeBetween(column="Close", min_value=0),
        gx.expectations.ExpectColumnValuesToBeBetween(column="High", min_value=0),
        gx.expectations.ExpectColumnValuesToBeBetween(column="Low", min_value=0),
        gx.expectations.ExpectColumnValuesToBeBetween(column="Open", min_value=0),
        gx.expectations.ExpectColumnValuesToNotBeNull(column="Date"),
        gx.expectations.ExpectColumnValuesToBeOfType(column="Date", type_="datetime64[ns]"),
        gx.expectations.ExpectColumnValuesToNotBeNull(column="Stock_Ticker")
    ]

    # Validate each expectation
    validation_results = []
    for expectation in expectations:
        result = batch.validate(expectation)
        validation_results.append(result)

    return validation_results