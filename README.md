# face-detection-service
&nbsp;&nbsp;&nbsp;&nbsp;Video rendering service that allow detect faces in video and return aggregated data to the user: general the number of faces for all video frames. <br> 
&nbsp;&nbsp;&nbsp;&nbsp;Specification [here](https://drive.google.com/file/d/18dhLkJ_KdzJ45ItUVO0W6BM6nm1QyK7s/view?usp=sharing).

## Core technology stack
Flask, SQLAlchemy, Alembic, Opencv
## Installation
1. <b>Via Docker</b><br>
Clone the repository and execute `docker build . -t face-detection-service` inside repository. Then execute `docker run -p 8000:8000 -t face-detection-service`<br>
2. <b>Manually</b><br>
Clone the repository. In the terminal execute `pip3 install -r requierements.txt`, then `alembic upgrade head` and `python3 main.py`.
## Examples
1. Example of <i>processing</i> and <i>waiting</i> videos:<br>
![Screenshot from 2021-08-13 00-33-01_crop](https://user-images.githubusercontent.com/46371199/129261035-b003b096-9f48-4f32-ae2c-0f4565283475.png) <br>
2. Example of <i>canceled</i> and <i>completed</i> videos:<br>
![Screenshot from 2021-08-13 00-36-45_crop3](https://user-images.githubusercontent.com/46371199/129262778-272cd38b-61e0-4f35-949e-0568ccbd9467.png) <br>
   Command to kill processes on local machine (port 8000): `sudo kill $(lsof -t -i :8000)` 


