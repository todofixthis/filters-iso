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

# Adoption of the existing repo; remove in a follow-up PR once applied
import {
  id = "filters-iso"
  to = module.repository.github_repository.this
}

import {
  id = "filters-iso"
  to = module.repository.github_repository_vulnerability_alerts.this
}

import {
  id = "filters-iso"
  to = module.repository.github_repository_dependabot_security_updates.this
}

import {
  id = "filters-iso"
  to = module.repository.github_branch_default.this
}

import {
  id = "filters-iso:24623882"
  to = module.repository.github_repository_ruleset.trunk["develop"]
}

import {
  id = "filters-iso:24623877"
  to = module.repository.github_repository_ruleset.trunk["main"]
}
