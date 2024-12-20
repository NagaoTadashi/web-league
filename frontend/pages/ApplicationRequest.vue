<script setup>
import { ref } from 'vue';

const user = await getCurrentUser();
const idToken = await user.getIdToken();

const runtimeConfig = useRuntimeConfig();

const isErrorDialogVisible = ref(false);

const itemId = ref(-1);
const dialogApprove = ref(false);
const dialogDecline = ref(false);
const headers = ref([
    { title: 'チーム', align: 'start', key: 'name', sortable: false },
    { title: '年', key: 'year', sortable: false },
    { title: '月', key: 'month', sortable: false },
    { title: '日', key: 'day', sortable: false },
    { title: '開始', key: 'start_time', sortable: false },
    { title: '終了', key: 'end_time', sortable: false },
    { title: '場所', key: 'location', sortable: false },
    { title: '', key: 'actions', sortable: false },
]);

const { data: applicationRequests } = await useFetch(
    `${runtimeConfig.public.apiUrl}/application_requests/`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

async function approveApplicationRequest(id) {
    const approvedApplicationRequest = await $fetch(
        `${runtimeConfig.public.apiUrl}/approve_application_request/${id}/`,
        {
            method: 'POST',
        }
    );

    if (approvedApplicationRequest == null) {
        isErrorDialogVisible.value = true;
    }
    applicationRequests.value = applicationRequests.value.filter(
        (applicationRequest) => applicationRequest.id !== id
    );
}

async function declineApplicationRequest(id) {
    await $fetch(
        `${runtimeConfig.public.apiUrl}/decline_application_request/${id}/`,
        {
            method: 'POST',
        }
    );

    applicationRequests.value = applicationRequests.value.filter(
        (applicationRequest) => applicationRequest.id !== id
    );
}

function approveItem(item) {
    itemId.value = item.id;
    dialogApprove.value = true;
}

function closeApprove() {
    dialogApprove.value = false;
    nextTick(() => {
        itemId.value = -1;
    });
}

function approveItemConfirm() {
    approveApplicationRequest(itemId.value);
    closeApprove();
}

function declineItem(item) {
    itemId.value = item.id;
    dialogDecline.value = true;
}

function closeDecline() {
    dialogDecline.value = false;
    nextTick(() => {
        itemId.value = -1;
    });
}

function declineItemConfirm() {
    declineApplicationRequest(itemId.value);
    closeDecline();
}
</script>

<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="applicationRequests"
            :sort-by="[
                { key: 'year', order: 'desc' },
                { key: 'month', order: 'desc' },
                { key: 'day', order: 'desc' },
            ]"
        >
            <template v-slot:top>
                <v-toolbar class="px-2">
                    <v-toolbar-title
                        >他チームからの申し込み依頼</v-toolbar-title
                    >
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>

                    <v-dialog v-model="dialogApprove" max-width="500px">
                        <v-card
                            prepend-icon="mdi-alert-circle-outline"
                            title="この申し込みを承認してもよろしいですか？"
                        >
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    text="キャンセル"
                                    variant="plain"
                                    @click="closeApprove"
                                ></v-btn>
                                <v-btn
                                    color="primary"
                                    text="OK"
                                    variant="tonal"
                                    @click="approveItemConfirm"
                                ></v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-dialog v-model="dialogDecline" max-width="500px">
                        <v-card
                            prepend-icon="mdi-alert-circle-outline"
                            title="この申し込みを辞退してもよろしいですか？"
                        >
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    text="キャンセル"
                                    variant="plain"
                                    @click="closeDecline"
                                ></v-btn>
                                <v-btn
                                    color="primary"
                                    text="OK"
                                    variant="tonal"
                                    @click="declineItemConfirm"
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
                    class="me-2"
                    color="#4CAF50"
                    @click="approveItem(item)"
                    v-tooltip:top="'承認'"
                >
                    mdi-check-circle-outline
                </v-icon>
                <v-icon
                    color="#F44336"
                    class="me-2"
                    @click="declineItem(item)"
                    v-tooltip:top="'辞退'"
                >
                    mdi-close-circle
                </v-icon>
            </template>
            <template v-slot:no-data>
                現在、他チームからの申し込みはありません
            </template>
        </v-data-table>

        <v-dialog v-model="isErrorDialogVisible" max-width="750">
            <v-card
                prepend-icon="mdi-alert-circle-outline"
                title="この申し込みは直前でキャンセルされたため、マッチできませんでした。"
            >
                <v-card-actions>
                    <v-btn color="primary" @click="isErrorDialogVisible = false"
                        >閉じる</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
