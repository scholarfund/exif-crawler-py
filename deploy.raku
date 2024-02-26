#!/usr/bin/env rakudo

use v6;

constant $app_name = "exif-crawler";

sub MAIN(
    Str   $release_tag,
    Str  :$terraform_action = "plan", # "plan" or "apply"
    Bool :$messy,
    Str  :$terraform_plan = "", # Path to .tfplan if running terraform plan or apply
) {
    # Gut check that script is running from root directory of a git project
    chdir($?FILE.IO.dirname);
    if !"./.git".IO.d {
        die("Expected to find a .git folder. Is this script in the right location?\n");
    }

    my $target_env = $release_tag.split("-").tail;
    my $terraform_plan_abs = "";

    if $terraform_plan ne "" {
        $terraform_plan_abs = IO::Spec::Unix.rel2abs($terraform_plan);
    }

    chdir "./terraform";

    if !"./$target_env.tfvars".IO.f {
        die("Missing $target_env.tfvars.\n");
    }

    # If --messy has not been specified, ensure that the git project is clean
    (run(<git diff-index --quiet HEAD>, :out, :err).exitcode == 0 || $messy)
        or die("Changes in tracked files since last commit. Use --messy to ignore.\n");

    # Configure Terraform to use the correct state file, depending on target environment
    run(
        <terraform init --reconfigure --lockfile=readonly>,
        "--backend-config=prefix=$app_name/$target_env",
    );

    if $terraform_action eq "plan" {
        if $terraform_plan_abs {
            run(
                "terraform",
                "plan",
                "--var-file=./$target_env.tfvars",
                "--var=image_tag=$release_tag",
                "--out=$terraform_plan_abs",
            );
        } else {
            run(
                "terraform",
                "plan",
                "--var-file=./$target_env.tfvars",
                "--var=image_tag=$release_tag",
            );
        }
    } elsif $terraform_action eq "apply" {
        if $terraform_plan_abs {
            run(
                "terraform",
                "apply",
                $terraform_plan_abs,
            );
        } else {
            run(
                "terraform",
                "apply",
                "--var-file=./$target_env.tfvars",
                "--var=image_tag=$release_tag",
            );
        }
    }
}
