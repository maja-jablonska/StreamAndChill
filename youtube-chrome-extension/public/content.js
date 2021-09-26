console.log("Executing content.js")

createOverlay = () => {
	var div = document.createElement("div");
	div.setAttribute("id", "StreamAndChillPlugin");
	div.style.width = "100px";
	div.style.height = "100px";
	div.innerHTML = "Hello";
	document.body.appendChild(div);
}

chrome.runtime.onMessage.addListener((message, _sender, _sendResponse) => {
	console.log("message :>> ", message);
	console.log("_sender :>> ", _sender);
	console.log("_sendResponse :>> ", _sendResponse);
        if (request.requested == "createDiv"){
            createOverlay()
            sendResponse({confirmation: "Successfully created div"});
        }
    });


chrome.runtime.onMessage.addListener((message, _sender, _sendResponse) => {
	console.log("message :>> ", message);
	console.log("_sender :>> ", _sender);
	console.log("_sendResponse :>> ", _sendResponse);
	if (message.requested == "getCurrentTime"){
		console.log("Observer is working...")
		tabId = message.tabId
		let overlayCreated = false
		callback = () => {
			setTimeout(() => {
				const currentTime = document.querySelector(".ytp-time-current");
				if (currentTime) {
					splittedTime = currentTime.innerText.split(":")
					seconds = splittedTime[0] * 60 + splittedTime[1]
				}
				chrome.storage.local.get('startTimestamp', data => {
					if (data.startTimestamp && data.startTimestamp < seconds && !overlayCreated) {
						chrome.storage.local.set({startTimestamp: undefined})
						overlayCreated = true
						console.log("Creating overlay...", data.startTimestamp, seconds)
						// createOverlay()
						window.open("https://radiant-brook-58130.herokuapp.com/", "extension_popup", "width=700,height=500,status=no,scrollbars=yes,resizable=no");
					}
				})
				// var div = document.createElement("div");
				// div.style.width = "100px";
				// div.style.height = "100px";
				// div.innerHTML = "Hello";
				// document.body.appendChild(div);
			}, 5000)
			
		}

		const observer = new MutationObserver(callback);
		observer.observe(document.body, {
			subtree: true,
			attributes: false,
			childList: true,
		})
		_sendResponse({confirmation: "Successfully created div"});
	}
});