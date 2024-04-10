# in Docker, it is common to base a new image on a previously-created image
FROM python:3.10-bookworm

# Set the working directory in the image
WORKDIR /app

RUN apt-get update -qq && apt-get install ffmpeg -y

# install dependencies into the image - doing this first will speed up subsequent builds, as Docker will cache this step
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . .

# expose the port that the app is running on
EXPOSE 9696

# Run app.py when the container launches
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "-p", "9696"]