import datetime
from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import AzureCliCredential



# LOG INTO AZURE
credentials = AzureCliCredential()


# ARM ID INIT
subscription_id = "44ad0ad0-6513-43de-a596-0b293e83e53c"
resource_group_name = "demo"
vm_name = "terraformDemoVM"

arm_resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(subscription_id, resource_group_name, vm_name)

# CLIENT OBJECT
client = MonitorManagementClient(
    credentials,
    subscription_id
)

# QUERY RESULTS
for metric in client.metric_definitions.list(arm_resource_id):
    # azure.monitor.models.MetricDefinition
    print("{}: id={}, unit={}\n".format(
        metric.name.localized_value,
        metric.name.value,
        metric.unit
    ))


print("----------------------------------------------")

# FETCH METRICS
    # Get CPU total of yesterday for this VM, by hour

today = datetime.datetime.now().date()
yesterday = today - datetime.timedelta(days=1)

metrics_data = client.metrics.list(
    arm_resource_id,
    timespan="{}/{}".format(yesterday, today),
    interval='PT1H',
    metricnames='Percentage CPU',
    aggregation='Total'
)

# REFERENCE
    # print(client.metrics.models)
    # print(client.metrics.list)


print("CPU TOTAL OF 24 HOURS")
for item in metrics_data.value:
    # azure.mgmt.monitor.models.Metric
    print("{} ({})".format(item.name.localized_value, item.unit))
    for timeserie in item.timeseries:
        for data in timeserie.data:
            # azure.mgmt.monitor.models.MetricData
            print("{}: {}".format(data.time_stamp, data.total))


