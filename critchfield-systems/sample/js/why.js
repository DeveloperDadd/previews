const buttons = Array.from(document.querySelectorAll("#why-2556 .cs-button"));
for (const item of buttons) {
	const onClick = () => {
		item.classList.toggle("cs-active");
	};
	item.addEventListener("click", onClick);
}
