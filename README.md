# SEASON-UPC

This repository contains code and configuration for the software developed by UPC in the context of the SEASON project. A RAN xApp providing REST endpoints and xApp lifecycle code for the infrastructure reconfiguration is provided.

## Repository layout

- `core/`
  - `restapi.py` — REST API server exposing xApp endpoints.
  - `xapp_main.py` — main entrypoint for the xApp component.
  - `xapp_metadata.json` — xApp metadata used by the RIC.
- `config/`
  - `xapp_config.json` — runtime configuration for the xApp.
  - `xapp_endpoints.json` — endpoints configuration used by the REST API / service discovery.

## Description

The xApp complements the Telemetry Collector by providing a REST API exposing RAN reconfiguration procedures to external entities. In addition, it monitors a selected set of metrics that are regularly streamed to the Telemetry Collector for further analysis and decision-making procedures.

## Acknowledgement

Part of this development has been supported by the SNS SEASON Project (G.A: 101096120)