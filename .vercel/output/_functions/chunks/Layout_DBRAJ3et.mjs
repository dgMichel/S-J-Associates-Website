import { t as createComponent } from "./compiler_COik8im5.mjs";
import { C as createAstro, _ as addAttribute, c as renderSlot, d as renderTemplate, g as renderHead, i as renderComponent, v as createRenderInstruction } from "./server_DOagsnPa.mjs";
//#region node_modules/astro/dist/runtime/server/render/script.js
async function renderScript(result, id) {
	const inlined = result.inlinedScripts.get(id);
	let content = "";
	if (inlined != null) {
		if (inlined) content = `<script type="module">${inlined}<\/script>`;
	} else {
		const resolved = await result.resolve(id);
		content = `<script type="module" src="${result.userAssetsBase ? (result.base === "/" ? "" : result.base) + result.userAssetsBase : ""}${resolved}"><\/script>`;
	}
	return createRenderInstruction({
		type: "script",
		id,
		content
	});
}
//#endregion
//#region node_modules/@vercel/analytics/dist/astro/index.astro
createAstro("https://astro.build");
var $$Index$1 = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$Index$1;
	return renderTemplate`${renderComponent($$result, "vercel-analytics", "vercel-analytics", {
		"data-props": JSON.stringify(Astro.props),
		"data-params": JSON.stringify(Astro.params),
		"data-pathname": Astro.url.pathname
	})}${renderScript($$result, "D:/Final/car_rent-main/node_modules/@vercel/analytics/dist/astro/index.astro?astro&type=script&index=0&lang.ts")}`;
}, "D:/Final/car_rent-main/node_modules/@vercel/analytics/dist/astro/index.astro", void 0);
//#endregion
//#region node_modules/@vercel/speed-insights/dist/astro/index.astro
createAstro("https://astro.build");
var $$Index = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$Index;
	return renderTemplate`${renderComponent($$result, "vercel-speed-insights", "vercel-speed-insights", {
		"data-props": JSON.stringify(Astro.props),
		"data-params": JSON.stringify(Astro.params),
		"data-pathname": Astro.url.pathname
	})}${renderScript($$result, "D:/Final/car_rent-main/node_modules/@vercel/speed-insights/dist/astro/index.astro?astro&type=script&index=0&lang.ts")}`;
}, "D:/Final/car_rent-main/node_modules/@vercel/speed-insights/dist/astro/index.astro", void 0);
//#endregion
//#region src/layouts/Layout.astro
createAstro("https://astro.build");
var $$Layout = createComponent(($$result, $$props, $$slots) => {
	const Astro = $$result.createAstro($$props, $$slots);
	Astro.self = $$Layout;
	return renderTemplate`<html lang="en" data-astro-cid-ju4pidww><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="icon" type="image/svg+xml" href="src/assets/file-1.svg"><meta name="generator"${addAttribute(Astro.generator, "content")}><title>SJ & Associates - Premium Car Rental</title><meta name="description" content="SJ &amp; Associates offers Suzuki Ignis and Nissan Cube car rentals. Reliable vehicles, transparent pricing, and exceptional service."><meta name="keywords" content="car rental, rent a car, Suzuki Ignis, Nissan Cube, vehicle rental"><meta name="robots" content="index, follow"><meta property="og:title" content="SJ &amp; Associates - Premium Car Rental"><meta property="og:description" content="Reliable vehicles, transparent pricing, and exceptional service."><meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">${renderHead($$result)}</head><body data-astro-cid-ju4pidww>${renderSlot($$result, $$slots["default"])}${renderComponent($$result, "Analytics", $$Index$1, { "data-astro-cid-ju4pidww": true })}${renderComponent($$result, "SpeedInsights", $$Index, { "data-astro-cid-ju4pidww": true })}</body></html>`;
}, "D:/Final/car_rent-main/src/layouts/Layout.astro", void 0);
//#endregion
export { renderScript as n, $$Layout as t };
