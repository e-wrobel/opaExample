package system

main = allow

default allow = false

allow {
	input.method = "GET"
	input.url = ["allowed_url"]
	input.role = ["manager"]
}

