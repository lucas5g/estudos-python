const $chatMessages = Qs(".messages")
const $uniqueMessagesContainer = Qs(".unique-message-container")

const setRoomActive = room_id => {
  QsAll(".list-rooms li").forEach((el) => el.classList.remove("active"))

  Qs(`#room-${room_id}`).classList.add("active")
  Qs("#selected-room").value = room_id

}
async function getMessages(room_id) {
  const res = await fetch(`/${room_id}`)
  const html = await res.text()
  $chatMessages.innerHTML = html
  setRoomActive(room_id)
}

const sendMessage = async(data) => {
  console.log(data)

  const response = await fetch(`/${data.room_id}/send`, {
    method:"POST",
    headers:{
      "Content-Type": "application/json",
      // "X-CSRFToken": data.csrfmiddlewaretoken,
      "X-CSRFToken": data.csrfmiddlewaretoken,

    },
    body: JSON.stringify(data)
  })

  const html = await response.text()
  $uniqueMessagesContainer.insertAdjacentHTML("beforeend", html)
  console.log(html)

}

getMessages(1)

Qs(".send-message").addEventListener("submit", e => {
  e.preventDefault()
  const data = Object.fromEntries(new FormData(e.target).entries())
  sendMessage(data)
})