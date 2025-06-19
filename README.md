# Introduction

Disclaimer: Let me prefix with this, I did not have enough time to
do this task. I don't know what I'm doing with deep learning.
I had never trained a model before in my life.
This is only a *learning* experience, not a product I'd ship to anyone.

I also rushed a bit since I thought I was late, but turned out I wasn't.

# High-level ideas

I saw [this guide](https://blog.roboflow.com/how-to-train-yolov8-on-a-custom-dataset/) from roboflow.
And saw that they have support for [active learning](https://blog.roboflow.com/active-learning-workflow/).
So I thought I could get a free ride using their service...

My idea was to use their [workflows](https://roboflow.com/workflows/build)
to build an interactive application, where you can view a video stream
and the object detection, and submit feedback to the roboflow project.

However, I can't find to share the workflow publicly,
so I can't really demo that.
Instead I cloned a crappy command-line app, modified it a bit so it
prints out text on the command line.

# Training

This part was surprisingly easy.
I don't have a GPU, so I had to rent T4 instances from Google Colab.
It turned out training (with GPU) was faster than I thought (only 5 minutes for 25 epochs?).
The fact that you can do transfer learning was also new, and very cool.

I followed the roboflow guide mentioned above.
The training precedure is written down in [this Colab notebook](https://colab.research.google.com/drive/1KYjN4LKS7x4syVd6BQTazrPfKnayfxze?usp=sharing).
I didn't tune the training parameters much,
but judging from the training result, it turned out well anyway.

I didn't have time to train the classification bit, sorry about that...
I don't think it's that hard to do (though I don't know what's the best way to do that, train a different model?).

You can see the training results in the Colab notebook.
It's very messy since I didn't have time to delete the stuff
that was written there originally.

I uploaded the best weights to this repo at `training/best.pt`.

# Deployment

This part was actually way harder than training.
The "roboflow inference" container image was huge (> 17 GB extracted),
and almost filled my old hard drive.
I'm really sorry to whoever will have to test this code.
I hope you have enough disk space, RAM, and patience.

There's a `compose.yaml` file at the root of this repo,
just run it with `docker compose up`.
It will pull the images, run the server,
and give you the command to run the test app.

I'll also give it right here
`inference-dashboard-example/run.sh <VIDEO_DIR> <VIDEO_FILE>`
You need to have the video file on your local machine.
Then split the path to the video into directory and the file name
(for example "/path/to/file.mp4" would be split into "path/to" and "file.mp4").
To be honest, it's completely crazy.
And I haven't tested it because I don't have a Linux machine (sorry).
I couldn't find a nicer way to interact with the inference server in time.
Ideally there would be a web app, but I had to hack Docker instead.

When you run it, the tool will print out how many dishes and trays
it sees at a regular frame interval. It communicates with the
inference server via HTTP, so not the fastest thing.

# Feedback?

If someone has access to my [roboflow project](https://universe.roboflow.com/workspace-vxpni/test-4z0i5),
they would be able to access the workflows that allows you to
upload new images to the training set.
It's described [on their website](https://blog.roboflow.com/active-learning-workflow/).
I've tested it and it worked on my machine.

Althought this flow is not exactly what I want.
I thought I'd be able to fix the mistakes the model makes interactively.
But I couldn't find anything like that from web search so far.

# Summary

It was a fun learning experience.
I don't really understand the deep learning aspect, but this task
has some aspects which reminds me of the cloud engineer job I had.
The most time-consuming part was figure out how to fit all the work
that has been done into a Docker container.

Since I was in a rush, everything can break, all the links could be broken.
Please tell me if something has gone awry.

# End
