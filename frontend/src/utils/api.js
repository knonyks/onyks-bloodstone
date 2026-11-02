import axios from 'axios';
import router from '@/router';

const api = axios.create(
{
    baseURL: '/api',
    timeout: 5000
});

api.interceptors.request.use((config) => 
{
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
})

api.interceptors.response.use(
    (res) => res,
    (err) => {
    if (err.response?.status === 401) 
    {
        localStorage.removeItem('token')
        router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } })
    }
    return Promise.reject(err)
    }
)

export const repository = 
{
    info: async () =>
    {
        try 
        {
            const response = await api.get(`/repository/info`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    content: async (path = '') =>
    {
        try 
        {
            const response = await api.get(`/repository/content`,
            {
                params: 
                {
                    path: path
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    statistics: async () =>
    {
        try
        {
            const response = await api.get(`/repository/statistics`);
            return response;
        }
        catch (error)
        {
            throw error
        }
    }
}

export const suppliers = 
{
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/suppliers/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/suppliers`, { name }, { timeout: 30000 });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sort_by = 'id', sort_desc = false) =>
    {
        try 
        {
            const response = await api.get(`/suppliers`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sort_by: sort_by,
                    sort_desc: sort_desc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/suppliers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    update: async (id, supplier) =>
    {
        try 
        {
            const response = await api.patch(`/suppliers/${id}`, {name: supplier});
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/suppliers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const tables = 
{
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/tables/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    counts: async () =>
    {
        try 
        {
            const response = await api.get(`/tables/counts`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (name) =>
    {
        try
        {
            const response = await api.post(`/tables`, { name }, { timeout: 30000 });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = false) =>
    {
        try 
        {
            const response = await api.get(`/tables`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search || undefined,
                    sort_by: sortBy,
                    sort_desc: sortDesc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try
        {
            const response = await api.delete(`/tables/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    update: async (id, table) =>
    {
        try 
        {
            const response = await api.patch(`/tables/${id}`, {name: table});
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/tables/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const manufacturers = 
{
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/manufacturers/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    counts: async () =>
    {
        try 
        {
            const response = await api.get(`/manufacturers/counts`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/manufacturers`, { name }, { timeout: 30000 });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sort_by = 'id', sort_desc = false) =>
    {
        try 
        {
            const response = await api.get(`/manufacturers`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sort_by: sort_by,
                    sort_desc: sort_desc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/manufacturers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    update: async (id, manufacturer) =>
    {
        try 
        {
            const response = await api.patch(`/manufacturers/${id}`, {name: manufacturer});
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    get: async (id) =>
    {
        try 
        {
            const response = await api.get(`/manufacturers/${id}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const tags = 
{
    list: async (page = 1, limit = 10, search = null, sort_by = 'name', sort_desc = false) =>
    {
        try 
        {
            const response = await api.get(`/tags`, {
                params: 
                {
                    page: page,
                    limit: limit,
                    search: search,
                    sort_by: sort_by,
                    sort_desc: sort_desc
                }
            });
            return response
        } 
        catch (error) 
        {
            throw error
        }
    }
}

export const elements = 
{
    last_added: async () =>
    {
        try 
        {
            const response = await api.get(`/elements/last-added`);
            return response
        } 
        catch (error)
        {
            throw error
        }
    },
    count: async () =>
    {
        try 
        {
            const response = await api.get(`/elements/count`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    create: async (element, datasheets = []) =>
    {
        try
        {
            const formData = new FormData();
            const meta = datasheets.map((file, i) => {
                const existing = Array.isArray(element?.datasheets) && typeof element.datasheets[i] === "object" && element.datasheets[i] !== null
                    ? element.datasheets[i]
                    : {};
                return { ...existing, name: existing.name || file.name };
            });
            formData.append("element", JSON.stringify({ ...element, datasheets: meta }));
            datasheets.forEach((datasheet) => formData.append("files", datasheet));

            const response = await api.post(`/elements`, formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });
            return response;
        }
        catch (error)
        {
            throw error;
        }
    },
    list: async (page = 1, limit = 100, search = null, sort_by = "created_at", sort_desc = false) =>
    {
        try 
        {
            const response = await api.get(`/elements`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sort_by: sort_by,
                    sort_desc: sort_desc
                }
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    get: async (uuid) =>
    {
        try 
        {
            const response = await api.get(`/elements/${uuid}`);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    update: async (uuid, element, files = null) =>
    {
        try 
        {
            const formData = new FormData();
            formData.append('element', JSON.stringify(element));

            if (files)
            {
                (Array.isArray(files) ? files : [files]).forEach((file) =>
                {
                    formData.append('files', file);
                });
            }

            const response = await api.patch(`/elements/${uuid}`, formData,
            {
                headers: {'Content-Type': 'multipart/form-data'}
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    duplicate: async (uuid, element, files = null) =>
    {
        try 
        {
            const formData = new FormData();
            formData.append('element', JSON.stringify(element));

            if (files)
            {
                (Array.isArray(files) ? files : [files]).forEach((file) =>
                {
                    formData.append('files', file);
                });
            }

            const response = await api.post(`/elements/${uuid}/duplicate`, formData,
            {
                headers: {'Content-Type': 'multipart/form-data'}
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    delete: async (id) =>
    {
        try 
        {
            const response = await api.delete(`/elements/${id}`);
            return response
        } 
        catch (error) 
        {
            return error
        }
    }
}

export const auth = 
{
    login: async (username, password) =>
    {
        try
        {
            const form = new URLSearchParams({ username, password });
            const response = await api.post('/auth/login', form);
            return response
        }
        catch (error)
        {
            throw error
        }
    },
    me: async () =>
    {
        try
        {
            const response = await api.get('/auth/me');
            return response
        }
        catch (error)
        {
            throw error
        }
    }
}


export const users = 
{
    list: async (page = 1, limit = 10, search = null, sort_by = 'created_at', sort_desc = false) =>
    {
        try
        {
            const response = await api.get(`/users`, {
                params:
                {
                    page: page,
                    limit: limit,
                    search: search,
                    sort_by: sort_by,
                    sort_desc: sort_desc
                }
            });
            return response
        }
        catch (error)
        {
            throw error
        }
    },
    delete: async (id) =>
    {
        try
        {
            const response = await api.delete(`/users/${id}`);
            return response
        }
        catch (error)
        {
            throw error
        }
    },
    update: async (id, user) =>
    {
        try
        {
            const response = await api.patch(`/users/${id}`, user);
            return response
        }
        catch (error)
        {
            throw error
        }
    },
    create: async (user) =>
    {
        try
        {
            const response = await api.post(`/users`, user);
            return response
        }
        catch (error)
        {
            throw error
        }
    },
    
}


export const services = 
{
    repository,
    elements,
    tables,
    manufacturers,
    suppliers,
    users,
    tags,
    auth
}

window.x = services