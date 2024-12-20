<script setup>
import { ref } from 'vue';

const user = await getCurrentUser();
const idToken = await user.getIdToken();

const runtimeConfig = useRuntimeConfig();

const { data: applications } = await useFetch(
    `${runtimeConfig.public.apiUrl}/application_status/`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

const itemId = ref(-1);

const dialogDelete = ref(false);

const headers = ref([
    { title: '状態', align: 'start', key: 'status', sortable: false },
    { title: 'チーム', key: 'name', sortable: false },
    { title: '年', key: 'year', sortable: false },
    { title: '月', key: 'month', sortable: false },
    { title: '日', key: 'day', sortable: false },
    { title: '開始', key: 'start_time', sortable: false },
    { title: '終了', key: 'end_time', sortable: false },
    { title: '場所', key: 'location', sortable: false },
    { title: '', key: 'actions', sortable: false },
]);

async function deleteApplication(id) {
    await $fetch(`${runtimeConfig.public.apiUrl}/application/${id}/`, {
        method: 'DELETE',
    });

    applications.value = applications.value.filter(
        (application) => application.id !== id
    );
}

function deleteItem(item) {
    itemId.value = item.id;
    dialogDelete.value = true;
}

function closeDelete() {
    dialogDelete.value = false;
    nextTick(() => {
        itemId.value = -1;
    });
}

function deleteItemConfirm() {
    deleteApplication(itemId.value);
    closeDelete();
}

watch(dialogDelete, (val) => {
    val || closeDelete();
});
</script>

<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="applications"
            :sort-by="[
                { key: 'year', order: 'desc' },
                { key: 'month', order: 'desc' },
                { key: 'day', order: 'desc' },
            ]"
        >
            <template v-slot:top>
                <v-toolbar class="px-2">
                    <v-toolbar-title
                        >他チームの募集への申し込み状況</v-toolbar-title
                    >
                    <v-divider class="mx-4" inset vertical></v-divider>

                    <v-spacer></v-spacer>

                    <v-dialog v-model="dialogDelete" max-width="550px">
                        <v-card
                            prepend-icon="mdi-alert-circle-outline"
                            title="この申し込みをキャンセルしてもよろしいですか？"
                        >
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    text="キャンセル"
                                    variant="plain"
                                    @click="closeDelete"
                                ></v-btn>
                                <v-btn
                                    color="primary"
                                    text="OK"
                                    variant="tonal"
                                    @click="deleteItemConfirm"
                                ></v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>

            <template v-slot:[`item.name`]="{ item }">
                <span>{{ item.name }}</span>
                <span style="margin-left: 8px"></span>
                <a
                    v-if="item.instagram_user_name"
                    :href="`https://www.instagram.com/${item.instagram_user_name}/`"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <img
                        src="../public/icons8-インスタグラム.svg"
                        width="30"
                        height="30"
                        style="vertical-align: middle"
                    />
                </a>
                <a
                    v-if="item.X_user_name"
                    :href="`https://x.com/${item.X_user_name}/`"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <img
                        src="../public/icons8-ツイッターx.svg"
                        width="30"
                        height="30"
                        style="vertical-align: middle"
                    />
                </a>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
                <v-icon
                    v-if="item.status === '回答待ち'"
                    color="#F44336"
                    class="me-2"
                    @click="deleteItem(item)"
                    v-tooltip:top="'キャンセル'"
                >
                    mdi-cancel
                </v-icon>
            </template>
            <template v-slot:no-data>現在、申し込みはありません。</template>
        </v-data-table>
    </div>
</template>
