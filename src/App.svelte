<script>
  const modules = import.meta.glob('/src/routes/kb/**/+page.svx', { eager: true });
  const pages = Object.fromEntries(Object.entries(modules).map(([path, mod]) => [path.replace('/src/routes', '').replace('/+page.svx', ''), mod.default]));
  const pathname = window.location.pathname.replace(/\/$/, '') || '/kb';
  const Page = pages[pathname] ?? pages['/kb'];
</script>

<Page />
