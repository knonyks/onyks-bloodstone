export const models = 
{
    elements:
    {
        getModel: () =>
        {
            return {
                uuid: '',
                part_name: '',
                manufacturer: '',
                table: '',
                description: '',
                availability: '',
                value: '',
                created_at: '',

                library_reference: '',
                library_path: '',

                footprint_reference_1: '',
                footprint_reference_2: '',
                footprint_reference_3: '',

                footprint_path_1: '',
                footprint_path_2: '',
                footprint_path_3: '',

                tags: [],
                suppliers: {},

                datasheets: []
            }

        }
    },
    user:
    {
        getModel: () =>
        {
            return {
                id: '',
                name: '',
                surname: '',
                login: '',
                password: '',
                rank: '',
                expirationTime: '',
                createdAt: ''
            }
        }
    }
}