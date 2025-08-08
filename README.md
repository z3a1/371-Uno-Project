# Instructions

## Requirements

There are no required libraries to install and the required modules (i.e. Tkinter, Pickle, Sockets) have already been implemented within Python's prebuilt module. It is suggested to use the latest version of Python to work.

### Launch Server & Client

The server must be first opened running the command `py game_server.py` Which is then followed for the other clients running `ui_client.py` 

### How To Start

The game requires at least 2 people for the game to start. When clicking join game you will be left within a waiting room as seen below:

<img width="800" height="600" alt="Image" src="https://github-production-user-asset-6210df.s3.amazonaws.com/92056808/475833322-5320d91d-3240-438a-a08a-18eb53a83a6a.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250808%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250808T020651Z&X-Amz-Expires=300&X-Amz-Signature=3cfd458f7ff0c6ab6d22436972a701a67f8e16d688e913a4a15d77233240574a&X-Amz-SignedHeaders=host" />

Upon joining the game, depending on how many players are in the server the game can or can't be started
<img width="800" height="600" alt="Image" src="https://github-production-user-asset-6210df.s3.amazonaws.com/92056808/475833319-197b2608-8349-4d27-9293-5bbd000b58a4.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250808%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250808T020621Z&X-Amz-Expires=300&X-Amz-Signature=5e55907fbc6783c4e6c46a98494f56bacf1f2a1021e3733fbbb5e3c6ce7a3fcf&X-Amz-SignedHeaders=host" />
If the server recognizes that there are two players right now, it will present the option to all of the users that they can start the game
<img width="800" height="600" alt="Image" src="https://github-production-user-asset-6210df.s3.amazonaws.com/92056808/475833320-9f61e0b2-5f98-4ab5-b180-c2a1a9b4f90b.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250808%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250808T020901Z&X-Amz-Expires=300&X-Amz-Signature=9b000c2a2bcf123f0f3552d09bace70223b393121f56aa5076a8e0e0deb575b8&X-Amz-SignedHeaders=host" />

### The Game State

As soon as the button is clicked all players are put into the current game room which presents the current clients deck and how many cards the other players have where the black box indicates whos current turn it is for the other clients, the last card played and the actions a client can take

<img width="598" height="614" alt="Image" src="https://github-production-user-asset-6210df.s3.amazonaws.com/92056808/475834824-e751802c-6eee-47d6-ad1a-34eb20025fee.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250808%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250808T021320Z&X-Amz-Expires=300&X-Amz-Signature=ac33c43484de094eb9cdb7f0a41897f6e226112168ab3a2350924d5a2a9d304b&X-Amz-SignedHeaders=host" />

There are three screens that can pop up after the game, either a force disconnect from a user, the win or lose screen

<img width ="598" height = "614" src = "https://github-production-user-asset-6210df.s3.amazonaws.com/92056808/475834826-2a7c6613-8fff-4daa-a2f9-69d95129cb44.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250808%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250808T021312Z&X-Amz-Expires=300&X-Amz-Signature=747e29c5ff91ea05f3a2d86ff1ea425ea8d2cdc95c0b5187eb19f694e482978f&X-Amz-SignedHeaders=host"/>


<img width = "598" height = "614" src = "https://github-production-user-asset-6210df.s3.amazonaws.com/92056808/475834825-a9050786-802d-42bc-b580-6c1da2c634ec.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250808%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250808T021328Z&X-Amz-Expires=300&X-Amz-Signature=0b3eb7d20d3f7e25dcb5494225db6acb4eb09193adc3eddc91bbebe564bd7fa2&X-Amz-SignedHeaders=host"/>

<img width = "598" height = "614" src = "https://github-production-user-asset-6210df.s3.amazonaws.com/92056808/475834827-d2581965-2804-45d3-8da4-6213da18cdd6.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250808%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250808T021225Z&X-Amz-Expires=300&X-Amz-Signature=95eef3325b5872ce9c4946d88dac1bbe206c5119ef5e1052c37ccf68712d0624&X-Amz-SignedHeaders=host"/>

