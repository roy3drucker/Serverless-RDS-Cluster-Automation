# Ready for deployment

This repository contains the infrastructure and supporting Lambda code used to automate provisioning of RDS clusters from GitHub-driven requests.

## SAM deployment

The SAM template under `sam/template.yaml` powers the API Gateway, Lambda, and messaging resources. A default configuration file (`sam/samconfig.toml`) is included so that running `sam deploy` works without additional flags.

The configuration sets the default AWS Region to `us-east-1`. If you need to use a different region, update `sam/samconfig.toml` or set `AWS_REGION`/`AWS_DEFAULT_REGION` before invoking the SAM CLI.

```bash
cd sam
sam deploy --guided  # first run creates any required resources
```

Subsequent deploys can be run with `sam deploy` and will automatically pick up the saved configuration, including the region


dfdfdfsdf
