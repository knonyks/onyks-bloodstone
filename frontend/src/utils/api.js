import axios from 'axios';

const api = axios.create(
{
    baseURL: '/api',
    timeout: 5000,
    headers: 
    {
        'Content-Type': 'application/json',
    // 'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
});

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
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
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
    edit: async (id, table) =>
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
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = false) =>
    {
        try 
        {
            const response = await api.get(`/manufacturers`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
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
    edit: async (id, manufacturer) =>
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
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = false) =>
    {
        try 
        {
            const response = await api.get(`/suppliers`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
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
    edit: async (id, supplier) =>
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











export const elements = 
{
    lastAdded: async () =>
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
    // create: async (element, datasheet = null) =>
    // {
    //     try 
    //     {
    //         const formData = new FormData();

    //         formData.append('element', JSON.stringify(element));

    //         if (datasheet)
    //         {
    //             formData.append('datasheet', datasheet);
    //         }

    //         const response = await api.post(`/element/create`, formData,
    //         {
    //             headers: {'Content-Type': 'multipart/form-data'} 
    //         });
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // duplicate: async (id, element, datasheet = null) =>
    // {
    //     try 
    //     {
    //         const formData = new FormData();

    //         formData.append('element', JSON.stringify(element));

    //         if (datasheet)
    //         {
    //             formData.append('datasheet', datasheet);
    //         }

    //         const response = await api.post(`/element/duplicate/${id}`, formData,
    //         {
    //             headers: {'Content-Type': 'multipart/form-data'} 
    //         });
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // get: async (id) =>
    // {
    //     try 
    //     {
    //         const response = await api.get(`/element/${id}`);
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    list: async (page = 1, limit = 10, search = null, sortBy = "createdAt", sortDesc = false) =>
    {
        try 
        {
            const response = await api.get(`/elements`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
                }
            });
            return response
        } 
        catch (error) 
        {
            return error
        }
    },
    // edit: async (id, element, datasheet = null) =>
    // {
    //     try 
    //     {
    //         const formData = new FormData();
    //         formData.append('element', JSON.stringify(element));

    //         if (datasheet)
    //         {
    //             formData.append('datasheet', datasheet);
    //         }

    //         const response = await api.put(`/element/edit/${id}`, formData,
    //         {
    //             headers: {'Content-Type': 'multipart/form-data'}
    //         });
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // delete: async (id) =>
    // {
    //     try 
    //     {
    //         const response = await api.delete(`/element/delete/${id}`);
    //         return response
    //     } 
    //     catch (error) 
    //     {
    //         return error
    //     }
    // },
    // openDatasheet: (uuid) =>
    // {
    //     window.open(`/files/${uuid}.pdf`, '_blank');
    // }
}


export const users = 
{
    create: async (name) =>
    {
        try 
        {
            const response = await api.post(`/users`, name);
            return response
        } 
        catch (error) 
        {
            throw error
        }
    },
    list: async (page = 1, limit = 100, search = '', sortBy = 'id', sortDesc = true) =>
    {
        try 
        {
            const response = await api.get(`/users`, {
                params: {
                    page: page,
                    limit: limit,
                    search: search,
                    sortBy: sortBy,
                    sortDesc: sortDesc
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
    edit: async (id, supplier) =>
    {
        try 
        {
            const response = await api.patch(`/suppliers/${id}`, supplier);
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

export const services = 
{
    repository,
    elements,
    tables,
    manufacturers,
    suppliers,
    users
}

window.x = services.elements