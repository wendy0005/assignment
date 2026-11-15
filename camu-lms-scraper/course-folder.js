// Shared by the popup and service worker; directory handles stay in extension storage.
const courseFolderDB = () => new Promise((resolve, reject) => {
  const request = indexedDB.open('camu-course-folder', 1);
  request.onupgradeneeded = () => request.result.createObjectStore('handles');
  request.onsuccess = () => resolve(request.result);
  request.onerror = () => reject(request.error);
});

export async function courseFolderGet() {
  const db = await courseFolderDB();
  try {
    return await new Promise((resolve, reject) => {
      const request = db.transaction('handles').objectStore('handles').get('current_sem');
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  } finally { db.close(); }
}

export async function courseFolderSet(handle) {
  const db = await courseFolderDB();
  try {
    await new Promise((resolve, reject) => {
      const tx = db.transaction('handles', 'readwrite');
      tx.objectStore('handles').put(handle, 'current_sem');
      tx.oncomplete = resolve;
      tx.onerror = () => reject(tx.error);
      tx.onabort = () => reject(tx.error);
    });
  } finally { db.close(); }
}

export async function findCourseFile(root, courseCode, size, hash) {
  if (!/^BCL\d{4}$/i.test(courseCode)) throw new Error('Cannot identify the course code.');
  if (await root.queryPermission({ mode: 'read' }) !== 'granted') {
    throw new Error('Access to current_sem has expired. Reconnect it in the scraper.');
  }
  let course = null;
  for await (const [name, handle] of root.entries()) {
    if (handle.kind === 'directory' && name.toUpperCase().startsWith(courseCode.toUpperCase() + ' - ')) {
      if (course) throw new Error('More than one current_sem folder matches ' + courseCode);
      course = handle;
    }
  }
  if (!course) return false;
  async function scan(dir) {
    for await (const [, handle] of dir.entries()) {
      if (handle.kind === 'directory') { if (await scan(handle)) return true; }
      else {
        const file = await handle.getFile();
        if (file.size !== size || !file.size) continue;
        const bytes = await crypto.subtle.digest('SHA-256', await file.arrayBuffer());
        const digest = Array.from(new Uint8Array(bytes), b => b.toString(16).padStart(2, '0')).join('');
        if (digest === hash) return true;
      }
    }
    return false;
  }
  return scan(course);
}
