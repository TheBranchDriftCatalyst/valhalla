
[Congress Bill Processor](./data_providers/congress_bills/congress_bill_erd.MD)

- [ ] get domain names
  - wtf-congress.io
  - wtfcongress.io

- s3 storage connectors

- [ ] start nexus agent (multimodal reasoning agent)
    - pg loader
    - vector store loader

- whisper pipeline ASR
    - [ ] s3 storage connector
    - whisper processing bucket
    - [ ] start transcribing 

- pypi setup.
- in order to make this a bit more PaaS styled, i need to setup pypi for the private repos and then for the public ones such as, data_provider.api.congress_gov, public
- this makes sense to be something not hosted locally, as my local stack is currently too ephemeral.
- spin up a digital ocean machine routed through pypi.knowledgedump.space for a privat pypi repo with static route
- 

- integrate celery