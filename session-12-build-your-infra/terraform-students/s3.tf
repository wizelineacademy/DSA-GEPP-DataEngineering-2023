# GEPP - QUESTION - What is that "force_destroy = true" for? Lines 5 and 10

resource "aws_s3_bucket" "s12-bronze-layer" {
  bucket = "deb-s12-bronze-${var.deb_student}"
  force_destroy = true
}

resource "aws_s3_bucket" "s12-silver-layer" {
  bucket = "deb-s12-silver-${var.deb_student}"
  force_destroy = true
}

