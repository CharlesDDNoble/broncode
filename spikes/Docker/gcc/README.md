This folder contains a dockerfile for a gcc compiler docker image.

Build the image:
	docker build --tag test_gcc .

Then run the image
	docker run test_gcc
