import { UserInfo, ConversationRequest, ChatMessage } from "./models";

export async function conversationApi(options: ConversationRequest, abortSignal: AbortSignal): Promise<Response> {
    const response = await fetch("/conversation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            messages: options.messages
        }),
        signal: abortSignal
    });

    return response;
}

export async function getUserInfo(): Promise<UserInfo[]> {
    const response = await fetch('/.auth/me');
    if (!response.ok) {
        console.log("No identity provider found. Access to chat will be blocked.")
        return [];
    }

    const payload = await response.json();
    return payload;
}

export async function selectHistoryRequest(user: string): Promise<Response> {
    const response = await fetch("/selecthistory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user: user
        }),
    });

    return response;
}

export async function saveConversation(user: string, title: string, messages: ChatMessage[]): Promise<Response> {
    const response = await fetch("/saveconversation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user: user,
            title: title,
            messages: messages
        }),
    });

    return response;
}