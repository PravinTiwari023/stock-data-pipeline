from prefect import task
import great_expectations as gx
import pandas as pd

@task
def validate_data(data):
    context = gx.get_context()

    data_source = context.data_sources.add_pandas("pandas")
    data_asset = data_source.add_dataframe_asset(name="pd dataframe asset")

    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch definition")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": data})

    suite = context.suites.add(
        gx.core.expectation_suite.ExpectationSuite(name="expectations")
    )

    expectation = gx.expectations.ExpectColumnValuesToBeBetween(
        column="Close", min_value=0
    )

    validation_result = batch.validate(expectation)

    return validation_result