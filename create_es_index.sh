#!/bin/bash
#	云日志模板
hostname=`hostname`
if [[ -n "$1" ]];then
    hostname="$1"
fi

curl -XPUT http://$hostname:9200/_template/openstack_logs -d '{
  "template": "*-openstack_log",
  "order": 1,
  "settings": {
    "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
            "codec": "best_compression",
            "refresh_interval" : "30s",
            "translog.durability": "async",
            "translog.flush_threshold_size": "1024mb"
        }
  },
  "mappings": { 
	"openstack_log": {
      "_all": {
        "enabled": false
      },  
      "properties": {
        "id": {
            "type": "keyword"
        },
		"reqId": {
			"type": "keyword",
			"doc_values": false
		},
		"instanceId": {
			"type": "keyword",
			"doc_values": false
		},
		"module": {
			"type": "keyword"
		},
		"hostname": {
			"type": "keyword"
		},
		"hostip": {
			"type": "keyword"
		},
		"pid": {
			"index": "no",
			"doc_values": false,
			"type": "keyword"
		},
		"size": {
			"index": "no",
			"type": "long"
		},
		"logdate": {
			"format": "yyyy-MM-dd HH:mm:ss.SSS",
			"type": "date"
		},
		"message": {
			"type": "text"
		},
		"logKind": {
			"type": "keyword"
		},
		"logLevel": {
			"type": "keyword"
		},
		"logKindDetail": {
			"type": "keyword"
		},
		"service": {
			"type": "keyword"
		},
		"fileName": {
			"type": "keyword",
			"doc_values": false
		},
		"cluster": {
			"type": "keyword",
			"doc_values": false
		},
		"cloud_uuid": {
			"type": "keyword"			
		},
		"logPackage": {
			"type": "keyword",
			"doc_values": false
		},
		"isException": {
			"type": "keyword"
		},
		"exceptionRegTag": {
			"type": "keyword"
		},
		"logTemplateTag": {
			"type": "keyword"
		},
		"cabinet": {
			"type": "keyword"
		}
      }
	}	  
  },
  "aliases": {
        "openstack_log" : {}
  }
}'

#	非云日志模板
curl -XPUT http://$hostname:9200/_template/other_logs -d '{
    "order": 1,
    "template": "*-other_log",
    "settings": {
        "index": {
            "number_of_shards": "6",			
            "number_of_replicas": "1",
			      "codec": "best_compression",
			      "max_result_window": "10000000",
            "refresh_interval" : "30s",
            "translog.durability": "async",
            "translog.flush_threshold_size": "1024mb"
        }
    },
    "mappings": {
        "logs": {
            "properties": {
                "cluster": {
                    "type": "keyword"
                },
                "hostname": {
                    "type": "keyword"
                },
                "module": {
                    "type": "keyword"
                },
                "logDate": {
                    "format": "yyyy-MM-dd HH:mm:ss.SSS",
                    "type": "date"
                },
                "logLevel": {
                    "type": "keyword"
                },
                "hostIp": {
                    "type": "keyword"
                },
                "service": {
                    "type": "keyword"
                },
                "logFileName": {  
		    "doc_values": false,				
                    "type": "keyword"
                },
                "message": {
                    "type": "text"
                },
                "logPackage": {
                    "index": "no",
                    "doc_values": false,
                    "type": "keyword"
                }
            }
        }
    },
  "aliases": {
        "other_log" : {}
  }
}'

# 监控模板
curl -XPUT http://$hostname:9200/_template/monitor_data -d '{
    "order": 1,
    "template": "*-monitor_data",
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression",
			"max_result_window": "10000000",
    "refresh_interval" : "30s",
    "translog.durability": "async",
    "translog.flush_threshold_size": "1024mb"
        }
    },
    "mappings": {
        "data": {
            "properties": {
                "hostname": {
                    "doc_values": false,
                    "type": "keyword"
                },
                "logDate": {
                    "format": "yyyy-MM-dd HH:mm:ss",
                    "doc_values": false,
                    "type": "date"
                },
                "metric": {
                    "doc_values": false,
                    "type": "keyword"
                },		
                "id": {
                    "doc_values": false,
                    "index": "no",
                    "type": "keyword"
                },
                "region": {
                    "type": "keyword"
                },
		"ip": {
                    "type": "keyword"
                },
                "message": {
                    "index": "no",
                    "doc_values": false,
                    "type": "keyword"
                },
		"cloud_uuid": {
                    "type": "keyword"
                }
            }
        }
    },
  "aliases": {
        "monitor_data" : {}
  }
}'

#	异常模板
curl -XPUT http://$hostname:9200/_template/service_anomal_data -d '{
  "template": "*-service_anomal_data",
  "order": 1,
  "settings": {
    "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
            "codec": "best_compression"
        }
  },
  "mappings": {
    "anomal": {
      "_all": {
        "enabled": false
      },	    	  
      "properties": {
		"servicename": {
			"type": "keyword"
		},
		"module": {
			"type": "keyword"
		},	
		"hostname": {
			"type": "keyword"
		},
		"uuid": {
			"type": "keyword"
		},
		"hostip": {
			"type": "keyword"
		},
         "hosttype": {		
			"type": "keyword",
			"doc_values": false
		},           
		"region": {		
			"type": "keyword",
			"doc_values": false
		},
		"clouduuid": {
			"type": "keyword",
			"doc_values": false
		},
		"timestamp": {
			"format": "yyyy-MM-dd HH:mm",
			"type": "date"
		},
		"cabinet": {			
			"type": "keyword"
		},		
		"anomalynum": {
			"type": "long"
		},
		"interval": {			
			"type": "keyword",
			"doc_values": false
		}
      }
    }
  },
  "aliases": {
        "service_anomal_data" : {}
  }
}'



#	告警模板
curl -XPUT http://$hostname:9200/_template/metric_alarm_data -d '{
  "template": "*-metric_alarm_data",
  "order": 1,
  "settings": {
    "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
            "codec": "best_compression"
        }
  },
  "mappings": {
    "alarm": {
      "_all": {
        "enabled": false
      },	    	  
      "properties": {
		"metric": {
			"type": "keyword"
		},
		"hostname": {
			"type": "keyword"
		},
		"uuid": {
			"type": "keyword"                   
		},
		"hostip": {
			"type": "keyword"
		},
        "hosttype": {		
			"type": "keyword",
			"doc_values": false
		},
		"region": {
			"type": "keyword",
			"doc_values": false
		},
		"clouduuid": {
			"type": "keyword",
			"doc_values": false
		},
		"timestamp": {
			"format": "yyyy-MM-dd HH:mm",
			"type": "date"
		},
		"cabinet": {			
			"type": "keyword"
		},		
		"alarmnum": {
			"type": "long"
		},
		"interval": {			
			"type": "keyword",
			"doc_values": false
		}
      }
    }
  },
  "aliases": {
        "metric_alarm_data" : {}
  }
}'

#	cluster_health_report 新建索引

cluster_health_report='cluster_health_report'
curl -XPUT http://$hostname:9200/$cluster_health_report -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression"
        }
    },
    "mappings": {
        "report": {
            "properties": {
				"cluster": {
					"type": "keyword"
				},
				"cloud_uuid": {
					"type": "keyword"					
				},
				"calTime": {
					"format": "yyyy-MM-dd HH:mm:ss",
					"type": "date"
				},
				"flag": {
					"type": "keyword",
					"doc_values": false
				},
				"reportDate": {
					"format": "yyyy-MM-dd",
					"type": "date"
				},
				"avgHealthDegree": {                    
					"type": "double"
				},
				"healthDegree": {                    
					"type": "double"
				},
				"actualNum": {                    
					"type": "double"
				},
				"targetNum": {                    
					"type": "double"
				},											
				"id": {
					"doc_values": false,
					"index": "no",
					"type": "keyword"
				}
            }
        }
    }
}'


#	host_health_report 新建索引

host_health_report='host_health_report'
curl -XPUT http://$hostname:9200/$host_health_report -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression"
        }
    },
    "mappings": {
        "report": {
            "properties": {
				"cluster": {
					"type": "keyword"
				},
				"cloud_uuid": {
					"type": "keyword"					
				},
				"hostname": {
					"type": "keyword"
				},
				"hostip": {
					"type": "keyword"
				},
				"calTime": {
					"format": "yyyy-MM-dd HH:mm:ss",
					"type": "date"
				},
				"flag": {
					"type": "keyword",
					"doc_values": false
				},
				"reportDate": {
					"format": "yyyy-MM-dd",
					"type": "date"
				},
				"avgHealthDegree": {                    
					"type": "double"
				},
				"healthDegree": {
					"type": "double"
				},
				"actualNum": {                    
					"type": "double"
				},
				"targetNum": {                    
					"type": "double"
				},
				"id": {
					"doc_values": false,
					"index": "no",
					"type": "keyword"
				}
            }
        }
    }
}'

#	service_health_report 模板

service_health_report='service_health_report'
curl -XPUT http://$hostname:9200/$service_health_report -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression"
        }
    },
    "mappings": {
        "report": {
            "properties": {
				"cluster": {
                    "type": "keyword"
				},
				"cloud_uuid": {
					"type": "keyword"					
				},
				"hostname": {
					"type": "keyword"
				},
				"hostip": {
					"type": "keyword"
				},
				"calTime": {
					"format": "yyyy-MM-dd HH:mm:ss",
					"type": "date"
				},
				"flag": {
					"type": "keyword",
					"doc_values": false
				},
				"reportDate": {
					"format": "yyyy-MM-dd",
					"type": "date"
				},
				"service": {
					"type": "keyword"
				},
				"avgHealthDegree": {                    
					"type": "double"
				},
				"healthDegree": {                    
					"type": "double"
				},
				"actualNum": {                    
					"type": "double"
				},
				"targetNum": {                    
					"type": "double"
				},
				"id": {
					"doc_values": false,
					"index": "no",
					"type": "keyword"
				}
            }
        }
    }
}'

#	periodic_task_health_report 模板
periodic_task_health_report='periodic_task_health_report'
curl -XPUT http://$hostname:9200/$periodic_task_health_report -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression"
        }
    },
    "mappings": {
        "report": {
            "properties": {
				"cluster": {
					"type": "keyword"
				},
				"cloud_uuid": {
					"type": "keyword"					
				},
				"periodicTask": {
					"type": "keyword"
				},
				"hostname": {
					"type": "keyword"					
				},
				"hostip": {
					"type": "keyword"
				},
				"period": {
					"index": "no",
					"type": "long",
					"doc_values": false
				},
				"calTime": {
					"format": "yyyy-MM-dd HH:mm:ss",
					"type": "date"
				},
				"reportDate": {
					"format": "yyyy-MM-dd",
					"type": "date"					
				},
				"service": {
					"type": "keyword"					
				},
				"targetNum": {					
					"type": "double",
					"doc_values": false
				},
				"healthDegree": {                    
					"type": "double"
				},
				"id": {
					"index": "no",
					"type": "string",
					"doc_values": false
				},
				"actualNum": {					
					"type": "long",
					"doc_values": false
				},
				"frequency": {					
					"type": "long",
					"doc_values": false
				}
            }
        }
    }
}'


#	periodic_task_interval_report 模板
periodic_task_interval_report='periodic_task_interval_report'
curl -XPUT http://$hostname:9200/$periodic_task_interval_report -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression"
        }
    },
    "mappings": {
        "report": {
            "properties": {
				"heartTime": {
					"format": "yyyy-MM-dd HH:mm:ss.SSS",
					"type": "date"
				},
				"cluster": {
					"type": "keyword",
					"doc_values": false
				},
				"cloud_uuid": {
					"type": "keyword"					
				},
				"periodicTask": {
					"type": "keyword",
					"doc_values": false
				},
				"hostname": {
					"doc_values": false,
					"type": "keyword"
				},
				"period": {
					"doc_values": false,
					"index": "no",
					"type": "long"
				},
				"calTime": {
					"format": "yyyy-MM-dd HH:mm:ss",
					"type": "date"
				},
				"reportDate": {
					"format": "yyyy-MM-dd",
					"doc_values": false,
					"type": "date"
				},
				"service": {
					"doc_values": false,
					"type": "keyword"
				},
				"timeInterval": {
					"doc_values": false,
					"index": "no",
					"type": "long"
				},
				"id": {
					"doc_values": false,
					"index": "no",
					"type": "keyword"
				},
				"frequency": {
					"doc_values": false,
					"index": "no",
					"type": "long"
				}
            }
        }
    }
}'


#	operation_log_report 模板

operation_log_report='operation_log_report'
curl -XPUT http://$hostname:9200/$operation_log_report -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression"
        }
    },
    "mappings": {
        "report": {
            "properties": {
                "cluster": {
					"type": "keyword",
					"doc_values": false
				},
				"cloud_uuid": {
					"type": "keyword"					
				},
				"updateTime": {
					"doc_values": false,
					"format": "yyyy-MM-dd HH:mm:ss",
					"type": "date"
				},
				"reqId": {
					"type": "keyword",
					"doc_values": false
				},
				"hostname": {
					"type": "keyword"
				},
				"instanceId": {
					"doc_values": false,
					"type": "keyword"
				},
				"createTime": {
					"format": "yyyy-MM-dd HH:mm:ss",
					"type": "date"
				},
				"useTime": {
					"type": "long"
				},
				"operationType": {
					"type": "keyword"
				},
				"startTime": {
					"format": "yyyy-MM-dd HH:mm:ss.SSS",
					"type": "date"
				},
				"detail": {
					"type": "keyword",
					"doc_values": false
				},
				"endTime": {
					"format": "yyyy-MM-dd HH:mm:ss.SSS",
					"type": "date"
				},
				"id": {
					"doc_values": false,
					"index": "no",
					"type": "keyword"
				},
				"status": {
					"type": "keyword"
				}
            }
        }
    }
}'

#	operation_stage_log_report 索引
operation_stage_log_report='operation_stage_log_report'
curl -XPUT http://$hostname:9200/$operation_stage_log_report -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1",
			"codec": "best_compression"
        }
    },
    "mappings": {
        "report": {
            "properties": {
                "cluster": {
					"type": "keyword",
					"doc_values": false
				},
				"cloud_uuid": {
					"type": "keyword"					
				},
				"operationStatus": {
					"type": "keyword"
				},
				"baseLogId": {
					"type": "keyword",
					"doc_values": false
				},
				"flag": {
					"type": "keyword",
					"doc_values": false
				},
				"logLevel": {
					"type": "keyword",
					"doc_values": false
				},
				"logDate": {
					"format": "yyyy-MM-dd HH:mm:ss.SSS",
					"type": "date"
				},
				"description": {
					"type": "keyword",
					"doc_values": false
				},
				"message": {
					"type": "text"
				},
				"regExp": {
					"type": "keyword",
					"doc_values": false
				},
				"reqId": {
					"type": "keyword",
					"doc_values": false
				},
				"hostname": {
					"type": "keyword"
				},
				"service": {
					"type": "keyword"
				},
				"useTime": {
					"type": "long"
				},
				"operationType": {
					"type": "keyword"
				},
				"startTime": {
					"format": "yyyy-MM-dd HH:mm:ss.SSS",
					"type": "date"
				},
				"endTime": {
					"format": "yyyy-MM-dd HH:mm:ss.SSS",
					"type": "date"
				},
				"id": {
					"doc_values": false,
					"index": "no",
					"type": "keyword"
				},
				"opStartTime": {
					"format": "yyyy-MM-dd HH:mm:ss.SSS",
					"type": "date"
				},
				"desc": {
					"type": "keyword",
					"doc_values": false
				}
            }
        }
    }
}'

#异常、告警  新建索引
yearmonth=`date +%Y%m`
metric_alarm_data=$yearmonth'-metric_alarm_data'
service_anomal_data=$yearmonth'-service_anomal_data'

curl -XPUT http://$hostname:9200/$metric_alarm_data -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1"
        }
    },
    "mappings": {
        "alarm": {
            "properties": {
					"metric": {
					"type": "keyword"
				},
				"hostname": {
					"type": "keyword"
				},
				"uuid": {
					"type": "keyword"                   
				},
				"hostip": {
						"type": "keyword"
				},
				"hosttype": {
						"type": "keyword",
						"doc_values": false
				},
				"region": {
						"type": "keyword",
						"doc_values": false
				},
				"clouduuid": {
						"type": "keyword",
						"doc_values": false
				},
				"timestamp": {
						"format": "yyyy-MM-dd HH:mm",
						"type": "date"
				},
				"cabinet": {
						"type": "keyword"
				},
				"alarmnum": {
						"type": "long"
				},
				"interval": {
						"type": "keyword",
						"doc_values": false
				}
            }
        }
    },
  "aliases": {
        "metric_alarm_data" : {}
  }
}'

curl -XPUT http://$hostname:9200/$service_anomal_data -d '{
    "settings": {
        "index": {
            "number_of_shards": "6",
            "number_of_replicas": "1"
        }
    },
    "mappings": {
        "anomal": {
            "properties": {
                "servicename": {
                        "type": "keyword"
                },
                "module": {
                        "type": "keyword"
                },
                "hostname": {
                        "type": "keyword"
                },
                "uuid": {
                        "type": "keyword"
                },
                "hostip": {
                        "type": "keyword"
                },
                 "hosttype": {
                        "type": "keyword",
                        "doc_values": false
                },           
                "region": {
                        "type": "keyword",
                        "doc_values": false
                },
                "clouduuid": {
                        "type": "keyword",
                        "doc_values": false
                },
                "timestamp": {
                        "format": "yyyy-MM-dd HH:mm",
                        "type": "date"
                },
                "cabinet": {
                        "type": "keyword"
                },
                "anomalynum": {
                        "type": "long"
                },
                "interval": {
                        "type": "keyword",
                        "doc_values": false
                }
            }
        }
    },
  "aliases": {
        "service_anomal_data" : {}
  }
}'


