export const models = 
{
    elements:
    {
        getModel: () =>
        {
            return {
                uuid: '',
                partName: '',
                manufacturer: '',
                table: '',
                description: '',
                availability: '',
                value: '',
                createdAt: '',

                libraryReference: '',
                libraryPath: '',

                footprintReferenceNo1: '',
                footprintReferenceNo2: '',
                footprintReferenceNo3: '',

                footprintPathNo1: '',
                footprintPathNo2: '',
                footprintPathNo3: '',

                tags: [],
                suppliers: {},

                datasheets: []
            }

        }
    }
}