type PageName = "input" | "output" | "settings";

const appRoot = document.querySelector<HTMLElement>("#app");
const pageCache = new Map<PageName, HTMLElement>();
const boundPages = new WeakSet<HTMLElement>();

function readPageFile(pageName: PageName): Promise<string> {
  const pageUrl = new URL(`./pages/${pageName}.html`, window.location.href);

  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();

    request.open("GET", pageUrl.href);
    request.addEventListener("load", () => {
      if (request.status === 0 || (request.status >= 200 && request.status < 300)) {
        resolve(request.responseText);
        return;
      }

      reject(new Error(`Failed to load page: ${pageName}`));
    });
    request.addEventListener("error", () => {
      reject(new Error(`Failed to load page: ${pageName}`));
    });
    request.send();
  });
}

async function loadPage(pageName: PageName): Promise<HTMLElement> {
  const cachedPage = pageCache.get(pageName);

  if (cachedPage) {
    return cachedPage;
  }

  const pageHtml = await readPageFile(pageName);
  const template = document.createElement("template");

  template.innerHTML = pageHtml.trim();

  const pageElement = template.content.firstElementChild;

  if (!(pageElement instanceof HTMLElement)) {
    throw new Error(`Invalid page markup: ${pageName}`);
  }

  pageCache.set(pageName, pageElement);
  return pageElement;
}

function bindPageButton(pageElement: HTMLElement, selector: string, pageName: PageName): void {
  pageElement.querySelectorAll<HTMLButtonElement>(selector).forEach((button) => {
    button.addEventListener("click", () => {
      void showPage(pageName);
    });
  });
}

function bindPageEvents(pageElement: HTMLElement): void {
  if (boundPages.has(pageElement)) {
    return;
  }

  bindPageButton(pageElement, '[data-action="open-settings"]', "settings");
  bindPageButton(pageElement, '[data-action="generate-html"]', "output");
  bindPageButton(pageElement, '[data-action="back-to-input"]', "input");
  bindPageButton(pageElement, '[data-action="cancel-settings"]', "input");
  bindPageButton(pageElement, '[data-action="save-settings"]', "input");
  bindPageButton(pageElement, '[data-action="return-input"]', "input");

  boundPages.add(pageElement);
}

async function showPage(pageName: PageName): Promise<void> {
  if (!appRoot) {
    throw new Error("App root element was not found.");
  }

  const pageElement = await loadPage(pageName);

  bindPageEvents(pageElement);
  appRoot.replaceChildren(pageElement);
}

void showPage("input");
