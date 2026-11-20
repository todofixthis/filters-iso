# This repo's GitHub configuration, provisioned by the todofixthis module (ADR 005).
terraform {
  required_version = ">= 1.9"

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

provider "github" {
  owner = "todofixthis"
}

module "repository" {
  source = "github.com/todofixthis/terraform-github-repository?ref=v1.1.0"

  description = "ISO extension for the Filters library"
  name        = "filters-iso"
}
