targetScope = 'resourceGroup'

@description('Globally unique short suffix for resource names, e.g. cwbdev001')
param nameSuffix string

@description('Azure region for all supported resources')
param location string = resourceGroup().location

@description('Cosmos DB database throughput. Keep <= 1000 RU/s to remain inside Cosmos DB free-tier allowance.')
@minValue(400)
@maxValue(1000)
param cosmosDatabaseThroughput int = 400

var prefix = 'cwb-${nameSuffix}'
var storageName = toLower(replace('cwb${nameSuffix}st', '-', ''))
var cosmosName = toLower('${prefix}-cosmos')
var functionName = toLower('${prefix}-api')
var staticWebAppName = toLower('${prefix}-web')
var appInsightsName = toLower('${prefix}-appi')

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    defaultToOAuthAuthentication: true
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
    SamplingPercentage: 10
  }
}

resource functionApp 'Microsoft.Web/sites@2023-12-01' = {
  name: functionName
  location: location
  kind: 'functionapp,linux'
  properties: {
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'Python|3.11'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storage.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${listKeys(storage.id, storage.apiVersion).keys[0].value}'
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'COSMOS_ENDPOINT'
          value: cosmos.properties.documentEndpoint
        }
        {
          name: 'COSMOS_DATABASE'
          value: database.name
        }
      ]
    }
  }
}

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: cosmosName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    enableFreeTier: true
    databaseAccountOfferType: 'Standard'
    publicNetworkAccess: 'Enabled'
    disableKeyBasedMetadataWriteAccess: true
    minimalTlsVersion: 'Tls12'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  parent: cosmos
  name: 'clan-war-board'
  properties: {
    resource: {
      id: 'clan-war-board'
    }
    options: {
      throughput: cosmosDatabaseThroughput
    }
  }
}

resource clans 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: database
  name: 'clans'
  properties: {
    resource: {
      id: 'clans'
      partitionKey: {
        paths: [ '/normalizedName' ]
        kind: 'Hash'
      }
    }
  }
}

resource wars 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: database
  name: 'wars'
  properties: {
    resource: {
      id: 'wars'
      partitionKey: {
        paths: [ '/clanPairKey' ]
        kind: 'Hash'
      }
    }
  }
}

resource summaries 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: database
  name: 'summaries'
  properties: {
    resource: {
      id: 'summaries'
      partitionKey: {
        paths: [ '/warId' ]
        kind: 'Hash'
      }
    }
  }
}

resource staticWebApp 'Microsoft.Web/staticSites@2023-12-01' = {
  name: staticWebAppName
  location: location
  sku: {
    name: 'Free'
    tier: 'Free'
  }
  properties: {
    allowConfigFileUpdates: true
  }
}

output functionAppName string = functionApp.name
output staticWebAppName string = staticWebApp.name
output cosmosAccountName string = cosmos.name
output cosmosDatabaseName string = database.name
