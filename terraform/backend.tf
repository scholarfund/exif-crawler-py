terraform {
  backend "gcs" {
    bucket = "tideswell-tfstate"
    prefix = "exif-crawler/prod"
  }
}
