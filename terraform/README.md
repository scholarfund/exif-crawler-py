# Deployment Configuration

This directory contains the infrastructure-as-code definitions for deploying
to staging or production. In order to do so successfully, adequate Google Cloud
Platform permissions are required.

## Troubleshooting

### Mismatched Terraform Versions

Command: `terraform apply <release_tag>.tfplan`

Error:
```
╷
│ Error: Failed to read plan from plan file
│
│ Cannot read the plan from the given plan file: plan file was created by Terraform 1.4.6, but this is 1.4.3-dev; plan files cannot be transferred between different Terraform versions.
```

Solution: Ensure that both the GitHub Actions workflow and the local machine are using the latest version of the Terraform CLI.

### Inconsistent Dependency Lock File

Command: `terraform apply <release_tag>.tfplan`

Error:
```
│ Error: Inconsistent dependency lock file
│
│ The given plan file was created with a different set of external dependency selections than the current configuration. A saved plan can be applied only to the same configuration it was created from.
│
│ Create a new plan from the updated configuration.
```

Solution: The local and remote provider lock files (`.terraform.lock.hcl`) are out of sync.
Ensure that there are no local changes from running `terraform init --upgrade` or similar.
This issue can be the result of caching provider plugins across different processor architectures.
Ensure that you have run
```bash
terraform providers lock -platform=darwin_amd64 -platform=darwin_arm64 -platform=linux_arm64 -platform=linux_amd64
```
with all appropriate platforms and committed the resulting lock file to version control.

### Error Acquiring State Lock

Command: `terraform plan`

Error:
```
│ Error: Error acquiring the state lock
│
│ Error message: writing "gs://tideswell-tfstate/zuiyo/prod/default.tflock"
│ failed: googleapi: Error 412: At least one of the pre-conditions you
│ specified did not hold., conditionNotMet
│ Lock Info:
│   ID:        1685988520877894
│   Path:      gs://tideswell-tfstate/zuiyo/prod/default.tflock
│   Operation: OperationTypePlan
│   Who:       runner@fv-az343-509
│   Version:   1.4.6
│   Created:   2023-06-05 18:08:40.802044526 +0000 UTC
│   Info:
│
│
│ Terraform acquires a state lock to protect the state from being written
│ by multiple users at the same time. Please resolve the issue above and try
│ again. For most commands, you can disable locking with the "-lock=false"
│ flag, but this is not recommended.
```

Solution: The shared state lock file in Google Cloud Storage is held by another
Terraform process. This can be due to a concurrent CI job or manual deployment,
but it can also be due to a previous Terraform command that failed to exit
cleanly. If the latter is the case, the `default.tflock` file can be deleted
manually in the `tideswell-tfstate` Google Cloud Storage bucket, using the
[web console](https://console.cloud.google.com/storage/browser/tideswell-tfstate;tab=objects).
