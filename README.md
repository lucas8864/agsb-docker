````markdown
# ArgoSB Docker for Hugging Face Spaces

## Overview
ArgoSB Docker is a lightweight Node.js service that sets up Argo tunnels and manages VLESS subscription links. It is containerized with Docker and can be deployed on **Hugging Face Spaces** or any Docker-compatible environment.  

It allows both temporary and fixed Argo tunnels, making it easy to expose services via Cloudflare Argo and manage subscription URLs for VLESS users.

## Features
- Runs ArgoSB scripts (`argosb.sh`) in a container
- Supports temporary and fixed Argo tunnels
- Auto-generates VLESS subscription links based on UUID and domain
- Lightweight Node.js 20 Alpine base image
- Easy deployment via Docker or Hugging Face Spaces

## Hugging Face Spaces Deployment

1. **Create a new Space** on Hugging Face using **Docker** runtime.
2. **Upload your project files** (including `Dockerfile`, `index.js`, `start.sh`, `argosb.sh`, `package.json`).
3. Ensure your `Dockerfile` is set to expose the container port used by your app (default `7860`):

```dockerfile
EXPOSE 7860
CMD ["node", "index.js"]
````

4. **Optional Environment Variables** (can be configured in Space settings):

   * `uuid` – your VLESS UUID
   * `vmpt` – VLESS WebSocket port
   * `hypt` – Hysteria port (if used)
   * `PORT` – internal container port (default `7860`)
   * `argo` – enable Argo tunnel (`y` or `n`)
   * `agn` – Argo domain for fixed tunnels
   * `agk` – Argo token/key for fixed tunnels

Hugging Face will automatically build the Docker image and run it, making your Space accessible via a public URL.

## Docker Deployment

1. Clone the repository:

```bash
git clone https://github.com/laalucas-us/agsb-docker.git
cd agsb-docker
```

2. Build the Docker image:

```bash
docker build -t argosb .
```

3. Run the container:

```bash
docker run -d --name argosb -p 7860:7860 \
  -e uuid="YOUR_UUID" \
  -e PORT=7860 \
  -e argo="y" \
  -e agn="example.com" \
  -e agk="ARGO_TOKEN" \
  argosb
```

4. Access the service at:

```
http://<server-ip>:7860
```

* Subscription links are available at `/YOUR_UUID` (or `/subuuid` if UUID is not set)
* Argo tunnel logs inside the container: `$HOME/agsb/argo.log`

## Folder Structure

```
├── Dockerfile
├── index.js
├── argosb.sh
├── start.sh
├── package.json
├── package-lock.json
└── README.md
```

## Notes

* Use **Node 20 Alpine** as the base for minimal image size.
* Ensure all scripts have **executable permissions** (`chmod +x argosb.sh start.sh`).
* `argosb.sh` is run by the Node.js process, so permissions and correct paths are important (`$HOME/agsb/argosb.sh`).

## Maintainer

* GitHub: [@laalucas-us](https://github.com/laalucas-us)
* Email: [laalucas88@gmail.com](mailto:laalucas88@gmail.com)
