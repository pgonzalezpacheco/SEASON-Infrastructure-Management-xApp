from xapp_lib import xapp_lib, actions
import restapi
import logging
import time

def main():
    builder = xapp_lib.XAppBuilder("..", absolute=False)
    builder.metadata("core/xapp_metadata.json")
    builder.endpoints("config/xapp_endpoints.json")
    builder.config("config/xapp_config.json")
    builder.readme("README.md")
    builder.restapi(
        [
            ("/api/resource_config", restapi.ResourceHandler)
        ]
    )
    xapp = builder.build()
    subscribe_to_topics(xapp)
    while True:
        try:
            process_data(xapp)
        except Exception as e:
            logging.error(e)
        

def subscribe_to_topics(xapp):
    xapp.kafka().subscribe([
        'accelleran.drax.5g.du_metrics.ue_mac',
        'accelleran.drax.5g.ric.raw.pm_counters',
        'resource-reconfiguration',
        ])

def log_message(message):
        logging.info(message)

def process_data(xapp):
        (topic, data) = xapp.kafka().json().recv_message()
        
        if data and 'resource-reconfiguration' in topic:
            print("Reached the handover function!")
            ue_id = data["ue_id"]
            cucp_id = data["cucp_id"]
            target_cell = actions.Cell(id=data["target_cell_id"], plmn="00101")
            try:
                actions.trigger_handover_5g(xapp=xapp, ue_id=ue_id, target_cell=target_cell,cucp_id=cucp_id)
            except Exception as e:
                print(f"Error triggering handover: {e}")
                
        elif data and topic == "accelleran.drax.5g.ric.raw.pm_counters":
            n_users = 0
            if data["topic"] == "cucp-0.CUCP_COUNTERS_INFO" and data["PmReportingCucpCounterData"]["CounterList"] != {}:
                for counter in data["PmReportingCucpCounterData"]["CounterList"]["items"]:
                    if data["PmReportingCucpCounterData"]["CounterList"]["items"][counter]["CounterId"] == "MEAN_NUMBER_OF_RRC_CONNECTIONS":
                        n_users = n_users + data["PmReportingCucpCounterData"]["CounterList"]["items"][counter]["ValueList"]["items"]["0"]["_val"]
                measurement = {"source": "ran", "n_users": n_users}
                print(measurement)
                xapp.kafka().json().send_message("season-demo-laq", measurement)
                time.sleep(1)
                
        else:
            print(data["DuUeMetrics"]["UlPuschRsrp"])

if __name__ == "__main__":
    main()