# Website of the Eclipse Conformity Assessment Policy and Credential Profile (Eclipse CAP)

The website is published at <https://eclipse-dataspace-cap.github.io/> 

## For Contributors

### Local build

For local build, use [act](https://github.com/nektos/act)

You can list actions with `act --list` and run a specific job with as below:


```shell
act --rm --job build --artifact-server-path public
unzip -o public/1/github-pages/github-pages.zip && tar xfv artifact.tar -C public
python3 -m http.server -d public
# and browse to http://localhost:8000
```
