Build a docker image with name "docker-form-send":
`docker build . -t docker-form-send`

---

Run contaner:
`docker run -p 3000:3000 -p 5000:5000 -v c:\!volume:/app/storage docker-form-send`
